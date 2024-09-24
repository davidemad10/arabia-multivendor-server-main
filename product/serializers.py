from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from .models import Brand,Category,Product,Review,Color,Size
from rest_framework import serializers

class BrandSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Brand)

    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = '__all__'




class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    class Meta:
        model=Review
        fields=['id','user','user_name','product','rating','review_text','created_at']
        read_only_fields = ['user', 'created_at']
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    def __init__(self, *args, **kwargs):
        super(ReviewSerializer,self).__init__(*args, **kwargs)

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']

class ProductSerializer(TranslatableModelSerializer):
    productName = serializers.CharField(source="translations.name")
    category = CategorySerializer()
    brand = BrandSerializer()
    translations = TranslatedFieldsField(shared_model=Product)
    description = serializers.CharField(source="translations.description" , read_only=True)
    specifications = serializers.JSONField()
    reviews = ReviewSerializer(many=True, read_only=True)
    # Add image fields
    thumbnail = serializers.ImageField(required=False, allow_null=True)
    image1 = serializers.ImageField(required=False, allow_null=True)
    image2 = serializers.ImageField(required=False, allow_null=True)
    image3 = serializers.ImageField(required=False, allow_null=True)
    image4 = serializers.ImageField(required=False, allow_null=True)
    color = ColorSerializer(many=True, read_only=True)
    size = SizeSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = "__all__"
        
    
    # def create(self, validated_data):
    #     reviews_data = validated_data.pop('reviews', [])
    #     product = Product.objects.create(**validated_data)
    #     for review_data in reviews_data:
    #         Review.objects.create(product=product, **review_data)
    #     return product
    # def update(self, instance, validated_data):
    #     reviews_data = validated_data.pop('reviews', [])
    #     instance = super().update(instance, validated_data)


from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from .models import Brand,Category,Product,Review,Color,Size,ProductImage
from rest_framework import serializers
from django.utils.translation import get_language

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
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['id','image','alt_text']

class ProductSerializer(TranslatableModelSerializer):
    productName = serializers.CharField(source="name")
    category = CategorySerializer()
    brand = BrandSerializer()
    translations = TranslatedFieldsField(shared_model=Product)
    description = serializers.CharField(source="translations.description" , read_only=True)
    specifications = serializers.JSONField()
    reviews = ReviewSerializer(many=True, read_only=True)
    images=ProductImageSerializer(many=True, read_only=True)
    color = ColorSerializer(many=True, read_only=True)
    size = SizeSerializer(many=True, read_only=True)
    image_uploads = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        reviews_data = validated_data.pop('reviews', [])
        image_data = validated_data.pop('image_uploads', [])
        product = Product.objects.create(**validated_data)
        for review_data in reviews_data:
            Review.objects.create(product=product, **review_data)
        for image in image_data:
            ProductImage.objects.create(product=product, image=image)
        return product
    def update(self, instance, validated_data):
        reviews_data = validated_data.pop('reviews', [])
        instance = super().update(instance, validated_data)


class ProductMinimalSerializer(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True, read_only=True)
    name = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','name', 'price_after_discount','images']
    def get_name(self, obj):
        # Use the current language code
        language = get_language()
        # Filter the translations for the current language
        translation = obj.translations.filter(language_code=language).first()
        return translation.name if translation else None
import json
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from .models import Brand,Category,Product,Review,Color,Size,ProductImage,ProductFact,CategoryDimension
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
    # Use PrimaryKeyRelatedField for writable actions (POST/PUT)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), write_only=True)
    color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all(), many=True, write_only=True)
    size = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all(), many=True, write_only=True)
    # Use detailed serializers for read-only actions (GET)
    category_details = CategorySerializer(source='category', read_only=True)
    brand_details = BrandSerializer(source='brand', read_only=True)
    color_details = ColorSerializer(source='color', many=True, read_only=True)
    size_details = SizeSerializer(source='size', many=True, read_only=True)

    translations = TranslatedFieldsField(shared_model=Product,required=False)
    description = serializers.CharField(source="translations.description" , read_only=True)
    specifications = serializers.JSONField()
    reviews = ReviewSerializer(many=True, read_only=True)
    image_uploads = serializers.ListField(
        child=serializers.ImageField(), write_only=True
    )
    images=ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):

        translations_data = validated_data.pop('translations', None)
        colors = validated_data.pop('color', [])
        sizes = validated_data.pop('size', [])
        reviews_data = validated_data.pop('reviews', [])
        image_data = validated_data.pop('image_uploads', [])

        # Create the product
        product = Product.objects.create(**validated_data)

        # Handle translations if available
        if translations_data:
            for lang, translation in translations_data.items():
                for field, value in translation.items():
                    setattr(product.translations, field, value)
            product.save()
        product.color.set(colors)
        product.size.set(sizes)
        for review_data in reviews_data:
            Review.objects.create(product=product, **review_data)
        for image in image_data:
            ProductImage.objects.create(product=product, image=image)
        return product
    def update(self, instance, validated_data):
        colors = validated_data.pop('color', [])
        sizes = validated_data.pop('size', [])
        image_data = validated_data.pop('image_uploads', [])
        reviews_data = validated_data.pop('reviews', [])
        instance = super().update(instance, validated_data)
        instance.color.set(colors)
        instance.size.set(sizes)
        if image_data:
            for image in image_data:
                ProductImage.objects.create(product=instance, image=image)
        return instance


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
    

class ProductFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFact  # Fact model for optimized retrieval
        fields = "__all__"

class CategoryDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryDimension  # Dimension model for optimized retrieval
        fields = "__all__"

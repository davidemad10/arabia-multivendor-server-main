from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from .models import Brand,Category,Product
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







class ProductSerializer(TranslatableModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = "__all__"


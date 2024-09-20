from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Address, BuyerProfile, SupplierProfile,SupplierDocuments
User = get_user_model()







class UserSerializer(serializers.ModelSerializer):
    # shipping_address = serializers.PrimaryKeyRelatedField(
    #     queryset=Address.objects.all(), many=False, required=False, allow_null=True
    # )

    created_date = serializers.SerializerMethodField(read_only=True)
    created_time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "is_buyer",
            "is_supplier",
            "created_date",
            "created_time",
            "password",
        )


    def get_created_date(self, obj):
        return obj.created.date()

    def get_created_time(self, obj):
        return obj.created.time()


    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)

    #     try:
    #         buyer_profile = instance.buyer_profile
    #         profile_serializer = BuyerProfileSerializer(instance=buyer_profile)
    #         representation["profile"] = profile_serializer.data
    #     except BuyerProfile.DoesNotExist:
    #         pass

    #     try:
    #         supplier_profile = instance.supplier_profile
    #         profile_serializer = SupplierProfileSerializer(instance=supplier_profile)
    #         representation["profile"] = profile_serializer.data
    #     except SupplierProfile.DoesNotExist:
    #         pass

    #     representation["shipping_address"] = AddressSerializer(
    #         instance=instance.shipping_address
    #     ).data
    #     representation["billing_address"] = AddressSerializer(
    #         instance=instance.billing_address
    #     ).data

    #     return representation


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class SupplierDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierDocuments
        fields = "__all__"





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["full_name"] = user.full_name
        # token["group_names"] = list(user.groups.values_list("name", flat=True))

        if user.parent is not None:
            token["parent"] = str(user.parent.id)
            token["role"] = "supplier" if user.is_supplier else "buyer"
        else:
            token["parent"] = None
            token["role"] = (
                "admin" if user.is_staff else "supplier" if user.is_supplier else "buyer"
            )

        try:
            if user.is_supplier:
                token["profile_picture"] = user.supplier_profile.profile_picture.url
            else:
                token["profile_picture"] = user.buyer_profile.profile_picture.url
        except ValueError:
            token["profile_picture"] = None

        return token

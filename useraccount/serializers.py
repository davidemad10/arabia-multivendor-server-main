from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Address, BuyerProfile, SupplierProfile,SupplierDocuments
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class BuyerProfileSerializer(serializers.ModelSerializer):
    phone= serializers.CharField(source='user.phone',read_only=True,max_length=15)
    class Meta:
        model=BuyerProfile
        fields=['id','phone','bank_account','instapay_account','electronic_wallet','profile_picture','favorite_products']

class UserSerializer(serializers.ModelSerializer):
    # shipping_address = serializers.PrimaryKeyRelatedField(
    #     queryset=Address.objects.all(), many=False, required=False, allow_null=True
    # )
    shipping_address=AddressSerializer(required=False)
    billing_address=AddressSerializer(required=False,read_only=True)
    password1=serializers.CharField(write_only=True,style={'input_type':'password'}, required=False)
    password2=serializers.CharField(write_only=True,style={'input_type':'password'}, required=False)
    created_date = serializers.SerializerMethodField(read_only=True)
    created_time = serializers.SerializerMethodField(read_only=True)
    buyer_profile = BuyerProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "created_date",
            "created_time",
            "password1",
            "password2",
            "phone",
            "shipping_address",
            "billing_address",
            "buyer_profile",
        )
        extra_kwargs = {
            'full_name': {'required': True, 'min_length': 1, 'max_length': 20},
            'email': {'required': True},
            'phone': {'required': True, 'allow_blank': False},
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove address fields if this is a registration request
        if self.context.get('request') and self.context['request'].method == 'POST':
            self.fields.pop('shipping_address', None)
            self.fields.pop('billing_address', None)
            self.fields.pop("buyer_profile",None)

    
    def validate_full_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Username cannot be empty")
        if len(value)>20:
            raise serializers.ValidationError("Username cannot be more than 20 characters")
        return value
    def validate_email(self,value):
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Email already exists")
        return  value
    def validate_phone(self, value):
        if value.startswith('+'):
            number = value[1:]
        else:
            number = value
        if not number.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits, except for the leading '+'.")
        if len(value) > 15:
                raise serializers.ValidationError("Phone number can not be more than 15 digits.")
        # Check if the phone number is not empty
        user_id = self.instance.id if self.instance else None
        if value and User.objects.filter(phone=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value
    def validate(self, data):
        password1=data.get('password1')
        password2=data.get('password2')
        if password1 or password2:
            if not password1:
                raise serializers.ValidationError({"password1":"password is required."})
            if not  password2:
                raise serializers.ValidationError({"password2":"password confirmation is required."})
            if password1 != password2:
                raise serializers.ValidationError({"password2":"passwords do not match."})
            try:
                validate_password(password1)
            except DjangoValidationError as e:
                raise serializers.ValidationError({"password1": list(e.messages)})
        return data
    def create(self,validated_data):
        password=validated_data.pop('password1',None)
        validated_data.pop('password2',None)
        user=User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def get_created_date(self, obj):
        return obj.created.date()

    def get_created_time(self, obj):
        return obj.created.time()

    def update(self, instance, validated_data):
        shipping_address_data = validated_data.pop('shipping_address', None)
        buyer_profile_data = validated_data.pop('buyer_profile', None)
        # Update user fields
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()

        # Update or create shipping_address if provided
        if shipping_address_data:
            if instance.shipping_address:
                # Update existing shipping address
                for key, value in shipping_address_data.items():
                    setattr(instance.shipping_address, key, value)
                instance.shipping_address.save()
            else:
                # Create new shipping address if it doesn't exist
                shipping_address = Address.objects.create(**shipping_address_data)
                instance.shipping_address = shipping_address
                instance.save()
        if buyer_profile_data is not None:
            buyer_profile, created = BuyerProfile.objects.get_or_create(user=instance)
            for key, value in buyer_profile_data.items():
                setattr(buyer_profile, key, value)
            buyer_profile.save()

        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["is_buyer"] = instance.is_buyer
        representation["is_supplier"] = instance.is_supplier
        if instance.shipping_address:
            representation["shipping_address"] = AddressSerializer(
                instance=instance.shipping_address
            ).data
        if instance.billing_address:
            representation["billing_address"] = AddressSerializer(
                instance=instance.billing_address
            ).data
        return representation


class SupplierDocumentsSerializer(serializers.ModelSerializer):
    front_id = serializers.FileField(required=True)
    back_id = serializers.FileField(required=True)
    tax_card = serializers.FileField(required=True)
    commercial_record = serializers.FileField(required=True)
    bank_statement = serializers.FileField(required=True)
    class Meta:
        model = SupplierDocuments
        fields = ['user','front_id','back_id','tax_card','commercial_record','bank_statement']




class SupplierProfileSerializer(serializers.ModelSerializer):
    phone= serializers.CharField(source='user.phone',max_length=15)
    entity_address=AddressSerializer()
    documents=SupplierDocumentsSerializer()
    class Meta:
        model=SupplierProfile
        fields=['id','phone','user','entity_address','bank_account','instapay_account','electronic_wallet','documents','profile_picture']



class SupplierRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    documents = SupplierDocumentsSerializer()
    address = AddressSerializer()
    class Meta:
        model=SupplierProfile
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

class VerfiyEmailserializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    otp=serializers.CharField(max_length=6)

class RequestotpSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)

class ResetPasswordWithOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

class  ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password=serializers.CharField(write_only=True, required=True)
    def  validate(self, data):
        new_password=data.get('new_password')
        confirm_password=data.get('confirm_password')
        if new_password  != confirm_password:
            raise serializers.ValidationError('The  two password fields must match.')
        return data
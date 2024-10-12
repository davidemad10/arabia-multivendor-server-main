from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Address, BuyerProfile, SupplierProfile,SupplierDocuments
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # shipping_address = serializers.PrimaryKeyRelatedField(
    #     queryset=Address.objects.all(), many=False, required=False, allow_null=True
    # )
    password1=serializers.CharField(write_only=True,style={'input_type':'password'}, required=False)
    password2=serializers.CharField(write_only=True,style={'input_type':'password'}, required=False)
    created_date = serializers.SerializerMethodField(read_only=True)
    created_time = serializers.SerializerMethodField(read_only=True)

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
        )
        extra_kwargs = {
            'full_name': {'required': True, 'min_length': 1, 'max_length': 20},
            'email': {'required': True},
            'phone': {'required': True, 'allow_blank': False},
        }
    def validate_full_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Username cannot be empty")
        if len(value)>20:
            raise serializers.ValidationError("Username cannot be more than 20 characters")
        return value
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
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
        if value and User.objects.filter(phone=value).exists():
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


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["is_buyer"] = instance.is_buyer
        representation["is_supplier"] = instance.is_supplier
        try:
            buyer_profile = instance.buyer_profile
            profile_serializer = BuyerProfileSerializer(instance=buyer_profile)
            representation["profile"] = profile_serializer.data
        except BuyerProfile.DoesNotExist:
            pass

        try:
            supplier_profile = instance.supplier_profile
            profile_serializer = SupplierProfileSerializer(instance=supplier_profile)
            representation["profile"] = profile_serializer.data
        except SupplierProfile.DoesNotExist:
            pass

        representation["shipping_address"] = AddressSerializer(
            instance=instance.shipping_address
        ).data
        representation["billing_address"] = AddressSerializer(
            instance=instance.billing_address
        ).data
        return representation

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class SupplierDocumentsSerializer(serializers.ModelSerializer):
    front_id = serializers.FileField(required=True)
    back_id = serializers.FileField(required=True)
    tax_card = serializers.FileField(required=True)
    commercial_record = serializers.FileField(required=True)
    bank_statement = serializers.FileField(required=True)
    class Meta:
        model = SupplierDocuments
        fields = ['user','front_id','back_id','tax_card','commercial_record','bank_statement']


class BuyerProfileSerializer(serializers.ModelSerializer):
    phone= serializers.CharField(source='user.phone',max_length=15)
    class Meta:
        model=BuyerProfile
        fields=['id','phone','bank_account','instapay_account','electronic_wallet','profile_picture','user','favorite_products']

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
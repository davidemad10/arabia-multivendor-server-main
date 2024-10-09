import json
import jwt
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
# from stats.models import Stats

# from .mixins import CheckBuyerAdminGroupMixin, CheckSupplierAdminGroupMixin
from .models import BuyerProfile, SupplierProfile, User,SupplierDocuments
from .serializers import (
    AddressSerializer,
    CustomTokenObtainPairSerializer,
    # StatsSerializer,
    UserSerializer,
    SupplierDocumentsSerializer,
    ResetPasswordWithOTPSerializer,
    RequestotpSerializer,
    VerfiyEmailserializer,
)
from .utils import send_temporary_password
import random
import string
from django.http import JsonResponse
from django.db import transaction


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
            response = super().post(request, *args, **kwargs)
            response_data = response.data
            token = response_data.get('access')
            refresh_token = response_data.get('refresh')
            # Set cookies for tokens
            response.set_cookie('access_token', token, httponly=True, secure=True, samesite='Lax')
            response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='Lax')
            # Return original response data
            response = JsonResponse({'done successfully': 'done successfully', 'tokens':response_data})
            return response



class BuyerRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        # Validate the serializer
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        password1 = data.get('password1')
        
        try:
            validate_password(password1)
        except ValidationError as e:
            return Response({'password_error': list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save(
                is_buyer=True,
                is_supplier=False,
                is_active=False, 
            )
            user.set_password(password1)
            user.save()
            BuyerProfile.objects.create(user=user)

        
            temp_password = ''.join(random.choices(string.digits, k=6))
            user.otp = temp_password 
            user.save() 

            send_temporary_password(
                temp_password,
                "emails/temp_password.html",
                _("Arbia Account Activation"),
                email,
            )
            return Response({
                'message': 'A temporary password has been sent to your email address.',
                'email': email
            }, status=status.HTTP_201_CREATED)



class VerifyOTPView(GenericAPIView):
    serializer_class= VerfiyEmailserializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.is_active = True  
            user.otp = None  # Clear the OTP after verification
            user.save()
            return Response({'message': 'Email successfully activated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

class RequestOTPview(GenericAPIView):
    serializer_class=RequestotpSerializer
    def post(self , request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        email = serializer.validated_data['email']
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        new_otp = ''.join(random.choices(string.digits, k=6))
        user.otp = new_otp 
        user.save()
        request.session['reset_email'] = email 
        send_temporary_password(
                new_otp,
                "emails/temp_password.html",
                _("Arbia Account Activation"),
                email,
            )
        return Response({
            'message': 'A new OTP has been sent to your email address.',
            'email': email
        }, status=status.HTTP_200_OK)

class ResetPasswordWithOTPview(GenericAPIView):
    serializer_class = ResetPasswordWithOTPSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        otp=serializer.validated_data['otp']
        new_password=serializer.validated_data['new_password']
        email=request.session.get('reset_email')
        if not email:
            return Response({'message': 'Session expired. Please request a new OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        if user.otp == otp:
            user.set_password(new_password)
            user.otp=None
            user.save()
            request.session.pop('reset_email',None)
            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)



class SupplierRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user_serializer = self.get_serializer(data=data)

        if user_serializer.is_valid():
            documents_serializer = SupplierDocumentsSerializer(data=data)
            address_serializer = AddressSerializer(data=data)

            if documents_serializer.is_valid() and address_serializer.is_valid():

                with transaction.atomic():
                    address = address_serializer.save()
                    documents = documents_serializer.save()
                    
                    user = user_serializer.save(
                        is_supplier=True,
                        is_active=False,
                    )
                    user.save()

                    SupplierProfile.objects.create(
                        user=user,
                        documents=documents,
                        entity_address=address
                    )

                    return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {
                        "documents_errors": documents_serializer.errors,
                        "address_errors": address_serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



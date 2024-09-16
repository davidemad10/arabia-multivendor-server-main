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
    SupplierDocumentsSerializer
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

        response = JsonResponse({'done successfully': 'done successfully'})
        response.set_cookie('access_token', token, httponly=True, secure=True, samesite='Lax')
        response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite='Lax')
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
        temp_password = ''.join(random.choices(string.digits, k=6))

        email = data.get('email')
        user = User.objects.filter(email__iexact=email).first()

        if user:
            user.set_password(temp_password)
            user.save()
        else:
            user = serializer.save(
                is_buyer=True,
                is_active=True, 
            )
            user.set_password(temp_password)
            user.save()
            BuyerProfile.objects.create(user=user)

        # send_temporary_password(
        #     temp_password,
        #     "emails/temp_password.html",
        #     _("Arbia Account Activation"),
        #     email,
        # )
        return Response({
            'message': 'A temporary password has been sent to your email address.',
            'email': email
        }, status=status.HTTP_201_CREATED)





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
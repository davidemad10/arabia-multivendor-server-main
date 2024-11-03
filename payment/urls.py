# payment/urls.py
from django.urls import path
from . import views
from .views import OrderpayInstapay

app_name = "payment"  # Add this line

urlpatterns = [
    path('instapay/', OrderpayInstapay.as_view(), name='payment-list-create'),
]

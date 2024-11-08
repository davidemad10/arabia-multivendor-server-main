from django.shortcuts import render
from .serializers import Paymentserializer
from .models import Payment
from order.models import  Order
from rest_framework import generics,status
from django.utils import timezone
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from order.models import *
from useraccount.models import *

class OrderpayInstapay(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = Paymentserializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Deserialize the data with the Payment serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the Payment instance
        payment = serializer.save()

        # Create the Order after successful payment
        cart = payment.cart  # Assuming `Payment` has a `cart` field
        user = request.user

        # Create a new Order
        order = Order.objects.create(
            user=user,
            cart=cart,
            is_paid=True,
            payment_method=payment.method,
            paid_date=timezone.now()
        )

        # Update the OrderItems based on CartItems
        cart_items = CartItem.objects.filter(cart=cart)
        order_items = []
        total_price = 0
        for item in cart_items:
            item_total_price = item.quantity * item.product.price_after_discount
            order_item = OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                total_price=item_total_price
            )
            order_items.append(order_item)
            total_price += item_total_price

            # Adjust stock
            product = item.product
            if item.quantity > product.stock_quantity:
                raise ValidationError(f"Insufficient stock for {product.name}.")
            product.stock_quantity -= item.quantity
            product.total_sold += item.quantity
            product.save()

        # Bulk create OrderItems
        OrderItem.objects.bulk_create(order_items)

        # Set the total price for the order
        order.total_price = total_price
        order.save()

        # Optionally mark the cart as completed (don't delete it)
        cart.status = 'completed'  # Assuming your Cart model has a status field
        cart.save()

        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Order created and payment successful.',
            'order_id': order.id,
            'total_price': order.total_price,
            'paid_date': order.paid_date,
        }, status=status.HTTP_201_CREATED, headers=headers)

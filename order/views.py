from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem, Cart , CartItem
from .serializers import(
    CreateOrderSerializer,
    OrderItemSerializer,
    CartSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    CartItemSerializer,
    OrderSerializer,
) 

# View for checking out a cart and creating an order
class CheckoutView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user_id': request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({
            'message': 'Order created successfully',
            'order_id': order.id,
            'total_price': order.total_price,
            'created': order.created,
        }, status=status.HTTP_201_CREATED)

# View for listing all order items of a user
class OrderItemListView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)

# View for listing all orders of a user
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

# View for retrieving a specific order
class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Order, id=self.kwargs["pk"], user=self.request.user)

# View for adding items to the cart
class AddCartItemView(generics.CreateAPIView):
    serializer_class = AddCartItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_item = serializer.save()
        return Response({
            'message': 'Item added to cart successfully',
            'item_id': cart_item.id,
            'quantity': cart_item.quantity,
        }, status=status.HTTP_201_CREATED)

# View for updating items in the cart
class UpdateCartItemView(generics.UpdateAPIView):
    serializer_class = UpdateCartItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()

    def get_object(self):
        return get_object_or_404(CartItem, id=self.kwargs["pk"], cart__items__cart__user=self.request.user)

# View for deleting items from the cart
class DeleteCartItemView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()

    def get_object(self):
        return get_object_or_404(CartItem, id=self.kwargs["pk"], cart__items__cart__user=self.request.user)

# View for retrieving the current user's cart
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Cart, items__cart__user=self.request.user)


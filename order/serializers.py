from rest_framework import serializers
from django.db import transaction
from .models import *
from product.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product= ProductSerializer(many=False)
    sub_total=serializers.SerializerMethodField()
    class Meta:
        model= CartItem
        fields = ['id','cart','product','quantity','sub_total']
    def get_sub_total(self,cartitem):
        return cartitem.quantity*cartitem.product.price_after_discount


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        return value
    
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"] 
        quantity = self.validated_data["quantity"] 
        
        try:
            cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            
            self.instance = cartitem
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")

        return self.instance


    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=["quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]
        
    def get_total_price(self, cart):
        return sum(item.quantity * item.product.price_after_discount for item in cart.items.all())


class OrderItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity","color","size","total_price"]
    def get_total_price(self, order_item):
        return order_item.get_final_price()


class OrderSerializer(serializers.ModelSerializer):
    order_items=OrderItemSerializer(many=True , read_only=True)
    total_price = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    class Meta:
        model = Order
        fields = ["id","is_paid","created","user","payment_method","total_price","order_items"]



class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("This cart_id is invalid")
        
        elif not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError("Sorry your cart is empty")
        
        return cart_id
    
    
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            order = Order.objects.create(user_id = user_id)
            cartitems = CartItem.objects.filter(cart_id=cart_id)
            orderitems = [
                OrderItem(order=order, 
                    product=item.product, 
                    quantity=item.quantity
                    )
            for item in cartitems
            ]
            OrderItem.objects.bulk_create(orderitems)
            Cart.objects.filter(id=cart_id).delete()
            order.get_total_order_price()
            
            return order


# class UpdateOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order 
#         fields = ["pending_status"]
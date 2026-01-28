
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Product
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

@action(detail=True, methods=['post'])
def add_item(self, request, pk=None):
    """Custom method to add or update a product in the cart"""
    cart = self.get_object()
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))

    product = get_object_or_404(Product, id=product_id)

    # Check if product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product
    )

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    
    cart_item.save()
    return Response({'status': 'Item added to cart'}, status=status.HTTP_201_CREATED)

@action(detail=True, methods=['post'])
def remove_item(self, request, pk=None):
    """Custom method to remove an item entirely from the cart"""
    cart = self.get_object()
    product_id = request.data.get('product_id')
    
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    
    return Response({'status': 'Item removed'}, status=status.HTTP_204_NO_CONTENT)

@action(detail=True, methods=['get'])
def summary(self, request, pk=None):
    """Returns a quick summary of total items and cost"""
    cart = self.get_object()
    total_price = sum(item.product.price * item.quantity for item in cart.items.all())
    total_items = sum(item.quantity for item in cart.items.all())
    
    return Response({
        'total_items': total_items,
        'total_price': total_price
    })
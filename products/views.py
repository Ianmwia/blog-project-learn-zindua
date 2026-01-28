from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Product
from .serializers import ProductsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response


#260126
class ProductPagination(PageNumberPagination):
    page_size = 5  # Number of items per page

# Create your views here.
class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

    #260126
    pagination_class = ProductPagination  # Add pagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Enable filtering and ordering
    search_fields = ['name']  # Fields to search through
    # http://127.0.0.1:8000/api/products/?search=chips
    # auth for admin@mail.com = Token 5893fd4e86c78577f787c2065c5c27e49fb3a1fe
    ordering_fields = ['price', 'created_at']  # Fields you can order by
    # decending pagination http://127.0.0.1:8000/api/products/?ordering=-price
    # different page pagination http://127.0.0.1:8000/api/products/?page=2
    permission_classes = [IsAuthenticated]
    def get():
        pass

class ExampleView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    def get(self, request):
        return Response({'message': 'This is a rate-limited view'})
# from advertisement.models import Advertisement
# from advertisement.serializers import AdvertisementSerializer
# from common.utils.create_slug import create_slug
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.db.models import Case, ExpressionWrapper, F, FloatField, Sum, When
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
# from openpyxl import load_workbook
from rest_framework import filters, status, viewsets,permissions
from rest_framework.generics import (
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .filters import ProductFilter
from .mixins import CheckProductManagerGroupMixin, CheckSupplierAdminGroupMixin
from .models import Brand,Category,Product,Review
from .pagination import ProductPagination
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
)
from django.http import Http404
from rest_framework.decorators import action
from django.utils.translation import activate
activate('en')  # or another language code


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()
    
    def list(self, request):
        featured = request.GET.get("featured")
        parent_slug = request.GET.get("parent")
        if featured == "true":
            queryset = self.queryset.filter(is_featured=True)
        else:
            try:
                queryset = self.queryset.all()
                if parent_slug:
                    queryset = self.queryset.filter(parent__slug=parent_slug)
            except Category.DoesNotExist:
                raise Http404 ('Category not found.')
        serializer = CategorySerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)




class BrandViewSet( viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # limit = int(request.GET.get("limit")) if request.GET.get("limit") else None
        # if limit:
        #     queryset = queryset[:limit]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class ProductViewSet( viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["created","name",]

    # filterset_class = ProductFilter
    # ordering = "name"
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category', 'brand').prefetch_related('color', 'size')
        queryset = queryset.filter(is_available=True, stock_quantity__gt=0)
        category_slug = self.request.GET.get("category")
        if category_slug:
            try:

                category=Category.objects.get(slug=category_slug)
                descendant_categories=category.get_descendants(include_self=False)
                queryset=queryset.filter(category__in=descendant_categories)
            except Category.DoesNotExist:
                    raise Http404 ('Category not found.')
        return queryset

    @action(detail=False, methods=["get"])
    def cached_products(self, queryset_key):
        cache_key = f'query_{queryset_key}'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = Product.objects.filter(is_available=True, stock_quantity__gt=0).select_related('category', 'brand')
            cache.set(cache_key, queryset, timeout=900) 
        return queryset

    @action(detail=True, methods=["get"])
    def you_may_like(self, request, pk=None):
        try:
            product = self.get_object()
            recommended_by_category = Product.objects.filter(
                category=product.category
            ).exclude(sku=product.sku).filter(is_available=True).order_by('-total_views')[:5]

            recommended_by_brand = Product.objects.filter(
                brand=product.brand
            ).exclude(sku=product.sku).filter(is_available=True).order_by('-total_views')[:5]

            recommended_products = (recommended_by_category | recommended_by_brand).distinct()[:5]

            serializer = ProductSerializer(recommended_products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Product.DoesNotExist:
            raise Http404('Product not found.')
    @action(detail=False, methods=["get"], url_path="bycategory")
    def get_products_by_category(self, request):
        category_slug = request.query_params.get("category")
        print("category_slug",category_slug)
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                # Get all descendant categories of the specified category
                descendant_categories = category.get_descendants(include_self=True)
                # Filter products within these categories
                products = Product.objects.filter(category__in=descendant_categories).order_by('id')
                print("Filtered products:", products)
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Category slug is required."}, status=status.HTTP_400_BAD_REQUEST)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the user and product when creating a review
        serializer.save(user=self.request.user)


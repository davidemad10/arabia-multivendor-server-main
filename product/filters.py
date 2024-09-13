from django.db.models import Q
from django_filters import BooleanFilter, CharFilter, FilterSet

from .models import Product


class CustomBooleanFilter(BooleanFilter):
    def filter(self, qs, value):
        if value is False:
            return qs

        return super().filter(qs, value)


class ProductFilter(FilterSet):
    name = CharFilter(lookup_expr="icontains")
    on_sale = CustomBooleanFilter(field_name="sale_price", lookup_expr="gt")
    category = CharFilter(field_name="category__parent__slug", lookup_expr="icontains")
    sub_category = CharFilter(field_name="category__slug", lookup_expr="icontains")
    brand = CharFilter(field_name="brand__name", lookup_expr="icontains")
    supplier = CharFilter(field_name="supplier__id", lookup_expr="iexact")

    class Meta:
        model = Product
        fields = [
            "name",
            "on_sale",
            "brand",
            "category",
            "sub_category",
        ]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        price_value_min = self.request.query_params.get("price_value_min")
        price_value_max = self.request.query_params.get("price_value_max")

        if price_value_min and price_value_max:
            queryset = queryset.filter(
                Q(price__range=(price_value_min, price_value_max))
                | Q(sale_price__range=(price_value_min, price_value_max))
                | Q(
                    price=0,
                    sale_price=0,
                    price_range_min__gte=price_value_min,
                    price_range_max__lte=price_value_max,
                )
            ).distinct()

        return queryset

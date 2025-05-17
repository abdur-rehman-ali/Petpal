import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Product Name")
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Min Price"
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Max Price"
    )
    is_available = django_filters.BooleanFilter(
        field_name="is_available", label="Available"
    )

    pet_category = django_filters.ChoiceFilter(
        choices=Product.PET_CATEGORY_CHOICES,
        label="Pet Category",
        empty_label="All Pet Categories",
    )

    product_type = django_filters.ChoiceFilter(
        choices=Product.PRODUCT_TYPE_CHOICES,
        label="Product Type",
        empty_label="All Product Types",
    )

    class Meta:
        model = Product
        fields = []

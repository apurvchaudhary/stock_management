"""
serializers
"""

from datetime import datetime

from decimal import Decimal
from django.utils import timezone

from rest_framework import serializers

from stock_app.models import SaleOrder, Product
from stock_app.constants import STOCK_LIMIT


def default_from():
    today = timezone.now().date()
    return timezone.make_aware(datetime.combine(today, datetime.min.time()))


def default_to():
    today = timezone.now().date()
    return timezone.make_aware(datetime.combine(today, datetime.max.time()))


class SaleOrderSerializer(serializers.ModelSerializer):
    """
    serializer class for sale Model
    """

    product = serializers.ReadOnlyField(source="product.name")
    supplier = serializers.ReadOnlyField(source="product.supplier.name")
    category = serializers.ReadOnlyField(source="product.category.name")
    date = serializers.SerializerMethodField()

    class Meta:
        """
        meta properties
        """

        model = SaleOrder
        fields = (
            "product",
            "total_price",
            "quantity",
            "supplier",
            "category",
            "date",
        )

    @staticmethod
    def get_date(obj):
        """
        method to format date
        :param obj:
        :return: str
        """
        return timezone.localtime(obj.sale_date).strftime("%d-%m-%Y at %H:%M")


class SaleOrderRangeSerializer(serializers.Serializer):
    """
    Serializer for query params for sales-views.
    Provides default values for `_from` and `_to` as the start and end of the current day.
    """

    _from = serializers.DateTimeField(default=default_from)
    _to = serializers.DateTimeField(default=default_to)
    limit = serializers.IntegerField(required=False, default=STOCK_LIMIT)


class ProductFilterSerializer(serializers.Serializer):
    category = serializers.IntegerField(required=False)
    price_operator = serializers.ChoiceField(choices=["=", ">", "<"], required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, min_value=Decimal("1.0"))

    def to_filter_kwargs(self):
        """
        Generate the filter kwargs for querying the Product model.
        This method only returns the filter arguments based on validated data.
        """
        filter_kwargs = {}
        category = self.validated_data.get("category")
        if category is not None:
            filter_kwargs["category_id"] = category
        price_operator = self.validated_data.get("price_operator")
        price = self.validated_data.get("price")
        if price_operator and price is not None:
            if price_operator == "=":
                filter_kwargs["price"] = price
            elif price_operator == ">":
                filter_kwargs["price__gt"] = price
            elif price_operator == "<":
                filter_kwargs["price__lt"] = price
        return filter_kwargs


class ProductSerializer(serializers.ModelSerializer):

    supplier_name = serializers.ReadOnlyField(source="supplier.name")
    category = serializers.ReadOnlyField(source="category.name")

    class Meta:
        """
        meta properties
        """

        model = Product
        fields = ("name", "price", "stock_quantity", "supplier_name", "category")

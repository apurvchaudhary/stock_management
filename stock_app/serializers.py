"""
serializers
"""

from datetime import datetime
from django.utils import timezone

from rest_framework import serializers

from stock_app.models import SaleOrder


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
    limit = serializers.IntegerField(required=False, default=None)

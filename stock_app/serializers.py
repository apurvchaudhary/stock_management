"""
serializers
"""
from datetime import date, timedelta

from rest_framework import serializers

from stock_app.models import Sell, Stock


class SellSerializer(serializers.ModelSerializer):
    """
    serializer class for sale Model
    """

    product = serializers.ReadOnlyField(source="product.name")
    brand = serializers.ReadOnlyField(source="product.brand.name")
    category = serializers.ReadOnlyField(source="product.category.name")
    date = serializers.SerializerMethodField()

    class Meta:
        """
        meta properties
        """

        model = Sell
        fields = ("product", "price", "quantity", "brand", "category", "date")

    @staticmethod
    def get_date(obj):
        """
        method to format date
        :param obj:
        :return: str
        """
        return obj.created_at.strftime("%d-%m-%Y/%H:%M")


class GetSellSerializer(serializers.Serializer):
    """
    serializer for query params for sales-views
    """

    _from = serializers.CharField(max_length=10, default=date.today().strftime("%Y-%m-%d"))
    _to = serializers.CharField(max_length=10, default=(date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))
    limit = serializers.IntegerField(required=False, default=None)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class StockSerializer(serializers.ModelSerializer):
    """
    serializer for Stock model
    """

    product = serializers.ReadOnlyField(source="product.name")
    category = serializers.ReadOnlyField(source="product.category.name")
    brand = serializers.ReadOnlyField(source="product.brand.name")

    class Meta:
        """
        meta properties
        """

        model = Stock
        fields = ("product", "category", "brand", "avg_buy_price", "quantity")

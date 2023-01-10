"""
utility module
"""
from datetime import date

from django.db.models import Sum

from stock_app.models import Sell, Product
from stock_app.serializers import SellSerializer


def get_sails(limit=None, _from=None, _to=None):
    """
    func to return recent sold product with given limit
    :return: orderDict
    """
    if _from and _to:
        sell = (
            Sell.objects.filter(created_at__range=[_from, _to])
            .select_related("product", "product__category", "product__brand")
            .order_by("-created_at")[:limit]
        )
    else:
        sell = Sell.objects.select_related("product", "product__category", "product__brand").order_by("-created_at")[
            :limit
        ]
    return SellSerializer(sell, many=True).data


def convert_date_dd_mm_yyyy(yyyy_mm_dd):
    """
    func to convert YYYY-MM-DD to DD-MM-YYYY
    :param yyyy_mm_dd: 2023-01-01
    :return: dd_mm_yyyy(01-01-2023)
    """
    return "-".join(yyyy_mm_dd.split("-")[::-1])


def get_month_sales_graph_data():
    """
    func to return month sales data
    :return: dict
    """
    sales = (
        Sell.objects.filter(created_at__month=date.today().month)
        .select_related("product")
        .values("product__name")
        .annotate(quantity=Sum("quantity"))
        .order_by("-quantity")
    )
    labels, data = [], []
    for sale in sales:
        labels.append(sale["product__name"]), data.append(sale["quantity"])
    return {"labels": labels, "data": data}


def get_least_and_most_selling_products():
    """
    func to return 10 most & least selling product
    :return:
    """
    most = [
        {"name": product["name"], "quantity": product["quantity"], "brand": product["brand__name"]}
        for product in Product.objects.prefetch_related("sell_set")
        .select_related("brand")
        .values("name", "brand__name")
        .annotate(quantity=Sum("sell__quantity"))
        .order_by("-quantity")[:10]
        if product["quantity"] is not None
    ]
    most_sold = [product["name"] for product in most]
    least = [
        {"name": product["name"], "quantity": product["quantity"], "brand": product["brand__name"]}
        for product in Product.objects.prefetch_related("sell_set")
        .values("name", "brand__name")
        .annotate(quantity=Sum("sell__quantity"))
        .order_by("quantity")[:10]
        if product["name"] not in most_sold
    ]
    return most, least

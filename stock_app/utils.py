"""
utility module
"""

from datetime import date

from django.db.models import Sum

from stock_app.models import SaleOrder, Product
from stock_app.serializers import SaleOrderSerializer, ProductSerializer


def get_sales(limit=None, _from=None, _to=None):
    """
    func to return recent sold product with given limit
    :return: orderDict
    """
    query = SaleOrder.objects.select_related("product", "product__category", "product__supplier").order_by("-sale_date")
    if _from and _to:
        query = query.filter(sale_date__range=[_from, _to])
    return SaleOrderSerializer(query[:limit], many=True).data


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
        SaleOrder.objects.filter(sale_date__month=date.today().month)
        .select_related("product", "product__supplier")
        .values("product__name", "product__supplier__name")
        .annotate(quantity=Sum("quantity"))
        .order_by("-quantity")
    )
    labels, data, count = [], [], 0
    for sale in sales:
        count += 1
        labels.append(f"{sale['product__name']} of {sale['product__supplier__name']}"), data.append(sale["quantity"])
    return {"labels": labels, "data": data, "count": count}


def get_least_and_most_selling_products():
    """
    func to return 10 most & least selling product
    :return:
    """
    most_selling = (
        SaleOrder.objects.select_related("product", "product__supplier")
        .values("product_id")
        .annotate(total=Sum("quantity"))
        .values("product__name", "total", "product__supplier__name")
        .order_by("-total")[:10]
    )
    least_selling = (
        SaleOrder.objects.select_related("product", "product__supplier")
        .values("product_id")
        .annotate(total=Sum("quantity"))
        .values("product__name", "total", "product__supplier__name")
        .order_by("total")[:10]
    )
    least_selling = [product for product in least_selling if product not in most_selling]
    return most_selling, least_selling


def get_products(filters):
    products = Product.objects.select_related("category", "supplier").filter(**filters)
    return ProductSerializer(products, many=True).data


def get_categories():
    return Product.objects.select_related("category").values("category_id", "category__name")

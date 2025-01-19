"""
views
"""

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stock_app.serializers import SaleOrderRangeSerializer, ProductFilterSerializer
from stock_app.utils import (
    get_sales,
    get_products,
    convert_date_dd_mm_yyyy,
    get_month_sales_graph_data,
    get_least_and_most_selling_products,
    get_categories,
)

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


@api_view()
def home_view(request):
    """
    View to get home page
    """
    most, least = get_least_and_most_selling_products()
    serializer = SaleOrderRangeSerializer(data={"limit": 10})
    if serializer.is_valid():
        return render(
            request,
            template_name="home.html",
            context={
                "recent_sale": get_sales(**serializer.data),
                "most_sales": most,
                "least_sales": least,
            },
        )


@api_view()
def sales_view(request):
    """
    View to get sales page
    """
    serializer = SaleOrderRangeSerializer(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        return render(
            request,
            template_name="sales.html",
            context={
                "recent_sale": get_sales(**serializer.validated_data),
                "from": convert_date_dd_mm_yyyy(serializer.data["_from"]),
                "to": convert_date_dd_mm_yyyy(serializer.data["_to"]),
            },
        )


@api_view()
def get_range_sales(request):
    serializer = SaleOrderRangeSerializer(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        return Response(get_sales(**serializer.validated_data))


@api_view()
def get_stock(request):
    return render(request, template_name="stock.html")


@api_view()
def fetch_products(request):
    serializer = ProductFilterSerializer(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        return Response(get_products(serializer.to_filter_kwargs()))


@api_view()
def sales_graph(request):
    """
    param : request
    return : json of labels and their data
    """
    return Response(get_month_sales_graph_data())


@api_view()
def get_all_category(request):
    return Response(get_categories())

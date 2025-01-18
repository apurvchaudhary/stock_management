"""
views
"""

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stock_app.serializers import SaleOrderRangeSerializer
from stock_app.utils import (
    get_sales,
    convert_date_dd_mm_yyyy,
    get_month_sales_graph_data,
    get_least_and_most_selling_products,
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
        pass
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
                "recent_sale": get_sales(**serializer.data),
                "from": convert_date_dd_mm_yyyy(serializer.data["_from"]),
                "to": convert_date_dd_mm_yyyy(serializer.data["_to"]),
            },
        )


# @api_view()
# def stock_view(request):
#     """
#     View to get stock page
#     """
#     request_offset = int(request.query_params.get("offset", 1))
#     offset = (request_offset - 1) * STOCK_LIMIT
#     _range = range(1, ceil(Stock.objects.count() / STOCK_LIMIT) + 1)
#     limit = offset + STOCK_LIMIT
#     return render(
#         request,
#         template_name="stock.html",
#         context={
#             "stocks": get_stocks(offset=offset, limit=limit),
#             "count": _range,
#             "max_offset": _range[-1],
#             "offset": request_offset,
#         },
#     )


@api_view()
def sales_graph(request):
    """
    param : request
    return : json of labels and their data
    """
    return Response(get_month_sales_graph_data())

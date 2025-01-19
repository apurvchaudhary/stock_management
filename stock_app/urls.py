"""
url patterns
"""

from django.urls import path

from stock_app.views import (
    home_view,
    sales_view,
    get_range_sales,
    sales_graph,
    get_stock,
    fetch_products,
    get_all_category,
)

# url paths
urlpatterns = [
    path("", home_view, name="home-view"),
    path("sales/", sales_view, name="sales-view"),
    path("sales-by-range/", get_range_sales, name="sales-by-range"),
    path("stock/", get_stock, name="stock-view"),
    path("products/", fetch_products, name="fetch-products"),
    path("graph/", sales_graph, name="graph-view"),
    path("categories/", get_all_category, name="all-categories"),
]

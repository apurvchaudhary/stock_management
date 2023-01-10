"""
url patterns
"""
from django.urls import path

from stock_app.views import home_view, sales_view, sales_graph, stock_view

# url paths
urlpatterns = [
    path("", home_view, name="home-view"),
    path("sales/", sales_view, name="sales-view"),
    path("stock/", stock_view, name="stock-view"),
    path("graph/", sales_graph, name="graph-view"),
]

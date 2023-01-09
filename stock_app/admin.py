from django.contrib import admin
from django.contrib.auth.models import Group, User

from stock_app.models import *

admin.site.unregister([Group, User])
admin.site.site_header = "Stock Management"
admin.site.site_title = "My Account"
admin.site.index_title = "My Data"
admin.site.site_url = "/"


class AdminCategory(admin.ModelAdmin):
    """
    django admin lookup
    """

    model = Category
    list_display = ("name", "description")


class AdminBrand(admin.ModelAdmin):
    """
    django admin lookup
    """

    model = Brand
    list_display = ("name", "description")


class AdminProduct(admin.ModelAdmin):
    """
    django admin lookup
    """

    model = Product
    list_display = ("name", "get_brand_name", "get_category_name", "get_quantity_count", "summary", "get_buy_price")

    @admin.display(ordering="-created_at", description="brand")
    def get_brand_name(self, obj):
        """
        method to get brand name
        :param obj: product
        :return: str
        """
        return obj.brand.name

    @admin.display(description="category")
    def get_category_name(self, obj):
        """
        method to get category name
        :param obj: product
        :return: str
        """
        return obj.category.name

    @admin.display(description="quantity in stock")
    def get_quantity_count(self, obj):
        """
        method to get quantity count
        :param obj: product
        :return: str
        """
        try:
            stock = Stock.objects.get(product=obj)
            return stock.quantity
        except ObjectDoesNotExist:
            return "0 or Not Added to Stock"

    @admin.display(description="Buy price")
    def get_buy_price(self, obj):
        try:
            stock = Stock.objects.get(product=obj)
            return stock.avg_buy_price
        except ObjectDoesNotExist:
            return "Not Added to Stock"


class AdminStock(admin.ModelAdmin):
    model = Stock
    list_display = ("get_product_name", "get_brand_name", "get_quantity", "avg_buy_price")

    @admin.display(ordering="-created_at", description="Product Name")
    def get_product_name(self, obj):
        """
        method to get stock's product name
        :param obj: stock
        :return: str
        """
        return obj.product.name

    @admin.display(description="brand Name")
    def get_brand_name(self, obj):
        """
        method to get stock's brand name
        :param obj: stock
        :return: str
        """
        return obj.product.brand.name

    @admin.display(description="quantity in stock")
    def get_quantity(self, obj):
        """
        method to get stock's product quantity
        :param obj: stock
        :return: str
        """
        return obj.quantity


class AdminPurchase(admin.ModelAdmin):
    model = Purchase
    list_display = (
        "get_product_name",
        "get_brand_name",
        "price",
        "quantity",
        "margin_percentage",
        "get_quantity_in_stock",
    )

    @admin.display(ordering="-created_at", description="Product Name")
    def get_product_name(self, obj):
        """
        method to get stock's product name
        :param obj: stock
        :return: str
        """
        return obj.product.name

    @admin.display(description="brand Name")
    def get_brand_name(self, obj):
        """
        method to get stock's brand name
        :param obj: stock
        :return: str
        """
        return obj.product.brand.name

    @admin.display(description="quantity in stock now")
    def get_quantity_in_stock(self, obj):
        """
        method to get quantity left in Stock
        :param obj: stock
        :return: int
        """
        try:
            stock = Stock.objects.get(product=obj.product)
            return stock.quantity
        except ObjectDoesNotExist:
            return "0 or Not Added to Stock"


class AdminSale(admin.ModelAdmin):
    model = Sell
    list_display = (
        "get_product_name",
        "get_brand_name",
        "price",
        "get_quantity_sold",
        "profit",
        "get_quantity_in_stock",
    )

    @admin.display(ordering="-created_at", description="Product Name")
    def get_product_name(self, obj):
        """
        method to get stock's product name
        :param obj: stock
        :return: str
        """
        return obj.product.name

    @admin.display(description="brand Name")
    def get_brand_name(self, obj):
        """
        method to get stock's brand name
        :param obj: stock
        :return: str
        """
        return obj.product.brand.name

    @admin.display(description="quantity sold")
    def get_quantity_sold(self, obj):
        """
        method to get quantity sold in this order
        :param obj: stock
        :return: int
        """
        return obj.quantity

    @admin.display(description="quantity in stock now")
    def get_quantity_in_stock(self, obj):
        """
        method to get quantity left in Stock
        :param obj: stock
        :return: int
        """
        try:
            stock = Stock.objects.get(product=obj.product)
            return stock.quantity
        except ObjectDoesNotExist:
            return "0 or Not Added to Stock"


admin.site.register(Category, AdminCategory)
admin.site.register(Brand, AdminBrand)
admin.site.register(Product, AdminProduct)
admin.site.register(Stock, AdminStock)
admin.site.register(Purchase, AdminPurchase)
admin.site.register(Sell, AdminSale)

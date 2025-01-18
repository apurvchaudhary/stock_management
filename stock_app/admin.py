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


class AdminSupplier(admin.ModelAdmin):
    """
    django admin lookup
    """

    model = Supplier
    list_display = ("name", "email", "phone", "address")


class AdminProduct(admin.ModelAdmin):
    """
    django admin lookup
    """

    model = Product
    list_display = (
        "name",
        "get_category_name",
        "get_quantity_count",
        "get_buy_price",
        "get_supplier_name",
        "description",
    )
    list_per_page = 10

    def get_queryset(self, request):
        """
        fetching category and supplier by JOIN
        """
        return Product.objects.select_related("category", "supplier")

    @admin.display(description="supplier")
    def get_supplier_name(self, obj):
        """
        method to get supplier name
        :param obj: product
        :return: str
        """
        return obj.supplier.name

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
        return obj.stock_quantity

    @admin.display(description="Buy price")
    def get_buy_price(self, obj):
        return obj.price


class AdminStockMovement(admin.ModelAdmin):
    list_display = ("product", "quantity", "movement_type", "movement_date")


class AdminSaleOrder(admin.ModelAdmin):
    list_display = ("product", "quantity", "status", "total_price", "sale_date")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["total_price"].disabled = True
        form.base_fields["total_price"].help_text = "Will be updated automatically."
        if obj and obj.status == "Pending":
            form.base_fields["status"].choices = SaleOrder.STATUS_CHOICES
        elif obj and obj.status != "Pending":
            for field_name in form.base_fields:
                form.base_fields[field_name].disabled = True
        else:
            form.base_fields["status"].disabled = True
        return form

    def save_model(self, request, obj, form, change):
        obj.total_price = obj.product.price * obj.quantity
        if obj.pk:
            previous_status = SaleOrder.objects.get(pk=obj.pk).status
            if previous_status == "Pending" and obj.status == "Completed":
                if obj.product.stock_quantity < obj.quantity:
                    form.add_error(
                        "quantity",
                        f"Not enough stock for {obj.product.name}. Current stock: {obj.product.stock_quantity}.",
                    )
                    return
                obj.product.stock_quantity -= obj.quantity
                obj.product.save()
        obj.save()


admin.site.register(Category, AdminCategory)
admin.site.register(Supplier, AdminSupplier)
admin.site.register(Product, AdminProduct)
admin.site.register(StockMovement, AdminStockMovement)
admin.site.register(SaleOrder, AdminSaleOrder)

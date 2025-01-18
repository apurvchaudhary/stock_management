from django.core.exceptions import ValidationError


def check_product_stock_quantity(product, quantity):
    if product.stock_quantity < quantity:
        raise ValidationError(
            {"quantity": f"Not enough stock available for {product.name}. Current stock is {product.stock_quantity}"}
        )

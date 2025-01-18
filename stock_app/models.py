"""
models
"""

from django.db import models, transaction
from django.db.models.manager import Manager
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, RegexValidator, EmailValidator
from stock_app.validators import check_product_stock_quantity


class TimeStampModel(models.Model):
    """
    model to save timestamp of created & updated
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Category(TimeStampModel):
    """
    model to save category
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    objects = Manager()

    def __str__(self):
        return self.name


class Supplier(TimeStampModel):
    """
    model to save Brand
    """

    name = models.CharField(max_length=255)
    email = models.EmailField(validators=[EmailValidator()], unique=True)
    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(r"^[0-9]{10}$", "Enter a valid 10-digit phone " "number.")],
        unique=True,
    )
    address = models.TextField(null=True, blank=True)

    objects = Manager()

    def __str__(self):
        return self.name


class Product(TimeStampModel):
    """
    model to save product
    """

    name = models.CharField(max_length=255, db_index=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.RESTRICT, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.PositiveIntegerField(default=0)

    objects = Manager()

    class Meta:
        unique_together = (
            "name",
            "supplier",
        )

    def __str__(self):
        return f"{self.name}, {self.stock_quantity} in stock."


class SaleOrder(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    sale_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    objects = Manager()

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    def clean(self):
        if self.quantity:
            check_product_stock_quantity(self.product, self.quantity)


class StockMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ("In", "In"),
        ("Out", "Out"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    movement_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    objects = Manager()

    def __str__(self):
        return f"{self.movement_type} - {self.product.name}"

    def clean(self):
        if self.quantity and self.movement_type == self.MOVEMENT_TYPE_CHOICES[1][0]:
            check_product_stock_quantity(self.product, self.quantity)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                previous_movement = StockMovement.objects.get(pk=self.pk)
                # Reverse the effect of the previous movement
                if previous_movement.movement_type == "In":
                    self.product.stock_quantity -= previous_movement.quantity
                elif previous_movement.movement_type == "Out":
                    self.product.stock_quantity += previous_movement.quantity

            # Apply the new movement (whether "In" or "Out")
            if self.movement_type == "Out":
                self.product.stock_quantity -= self.quantity
            elif self.movement_type == "In":
                self.product.stock_quantity += self.quantity

            self.product.save()
            super().save(*args, **kwargs)


class Stock(TimeStampModel):
    """
    model to save stock
    """

    product = models.OneToOneField(Product, on_delete=models.RESTRICT)
    quantity = models.IntegerField()
    avg_buy_price = models.DecimalField(null=True, max_digits=100, decimal_places=2)

    objects = Manager()


class Purchase(TimeStampModel):
    """
    model to save purchase orders
    """

    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    quantity = models.IntegerField()
    margin_percentage = models.DecimalField(null=True, max_digits=100, decimal_places=2)

    objects = Manager()

    def save(self, *args, **kwargs):
        try:
            stock = Stock.objects.get(product=self.product)
            stock.avg_buy_price = (stock.avg_buy_price * stock.quantity + self.price * self.quantity) / (
                stock.quantity + self.quantity
            )
            stock.quantity += self.quantity
            stock.save()
        except ObjectDoesNotExist:
            Stock.objects.create(product=self.product, quantity=self.quantity, avg_buy_price=self.price)
        super().save(*args, **kwargs)


class Sell(TimeStampModel):
    """
    model to save sell data
    """

    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    quantity = models.IntegerField()
    profit = models.DecimalField(null=True, max_digits=100, decimal_places=2)

    objects = Manager()

    def save(self, *args, **kwargs):
        stock = Stock.objects.get(product=self.product)
        stock.quantity -= self.quantity
        stock.save()
        self.profit = self.price * self.quantity - stock.avg_buy_price * self.quantity
        super().save(*args, **kwargs)

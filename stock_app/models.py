"""
models
"""
from django.db import models
from django.db.models.manager import Manager
from django.core.exceptions import ObjectDoesNotExist


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
    description = models.TextField(null=True)

    objects = Manager()

    def __str__(self):
        return self.name


class Brand(TimeStampModel):
    """
    model to save Brand
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)

    objects = Manager()

    def __str__(self):
        return self.name


class Product(TimeStampModel):
    """
    model to save product
    """

    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    summary = models.TextField(null=True)

    objects = Manager()

    def __str__(self):
        return f"{self.name} - {self.brand.name}"


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

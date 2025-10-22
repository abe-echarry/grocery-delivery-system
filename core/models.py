from django.db import models

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"


#address,order,orderitem
from django.conf import settings
from django.db import models

class Address(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=120)
    city  = models.CharField(max_length=60)
    state = models.CharField(max_length=40)
    zip   = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.line1}, {self.city}, {self.state} {self.zip}"

class Order(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    address    = models.ForeignKey(Address, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    total      = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} for {self.user}"

class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product    = models.ForeignKey('core.Product', on_delete=models.PROTECT)
    quantity   = models.PositiveIntegerField()
    price_each = models.DecimalField(max_digits=8, decimal_places=2)


from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):

    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class Order(models.Model):
    STATUS_CHOICES = (
        ("PAYMENT_PENDING", "Payment Pending"),
        ("PLACED", "Placed"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Customer details
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)

    # 🔥 NEW PAYMENT PROOF FIELDS
    utr_last6 = models.CharField(max_length=6, blank=True, null=True)
    payment_screenshot = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PAYMENT_PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    variant = models.ForeignKey("ProductVariant", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.variant.product.name} ({self.variant.size}) x{self.quantity}"



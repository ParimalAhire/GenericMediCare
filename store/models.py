from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):

    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')

    def is_customer(self):
        return self.user_type == 'customer'

    def is_admin(self):
        return self.user_type == 'admin'

    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def _str_(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    description = models.TextField()
    image_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    prescription_required = models.BooleanField(default=False)
    expiry_date = models.DateField()  # Added expiry date
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(Medicine, through="OrderItem")  # Added ManyToMany field
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)  # Added tracking number
    delivery_date = models.DateField(blank=True, null=True)  # Added expected delivery date
    delivery_address = models.TextField()  # Added delivery address
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)  # Added coupon field

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.code} - {self.discount_percentage}%"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Credit Card', 'Credit Card'),
        ('UPI', 'UPI'),
        ('Net Banking', 'Net Banking'),
        ('COD', 'COD')
    ]
    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded')
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='Pending')
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)

class Prescription(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_url = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)  # Added approval timestamp

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
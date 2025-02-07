from django.db import models
import datetime

# Category model
class Category(models.Model):
    category_name = models.CharField(max_length=255)
    category_description = models.TextField()
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = 'Categories'

# Customer model
class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    preferred_language = models.CharField(max_length=50, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=50, choices=[('regular', 'Regular'), ('admin', 'Admin'), ('pharmacist', 'Pharmacist')], default='regular')
    health_conditions = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

# Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField()
    dosage = models.TextField()
    side_effects = models.TextField(null=True, blank=True)
    active_ingredient = models.CharField(max_length=255, null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    brand_name = models.CharField(max_length=255, null=True, blank=True)
    image= models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.name

# Customer Orders
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_date = models.DateTimeField(default=datetime.datetime.now)    
    delivery_address = models.TextField()
    phone = models.CharField(max_length=20, default='', blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='pending')
    payment_status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending')
    shipment_tracking_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.name}"

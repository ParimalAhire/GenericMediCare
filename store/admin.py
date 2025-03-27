from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Medicine, Order, OrderItem, Payment, Prescription, Review

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_superuser')

# Register User model
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(Category)
admin.site.register(Medicine)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Prescription)
admin.site.register(Review)
from django.contrib import admin
from .models import Item, Order, ItemOrder
from Authentication.models import User
# Register your models here.


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    pass


@admin.register(Item)
class AdminItem(admin.ModelAdmin):
    pass


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    pass


@admin.register(ItemOrder)
class AdminItemOrder(admin.ModelAdmin):
    pass

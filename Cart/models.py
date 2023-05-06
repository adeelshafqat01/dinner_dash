from django.db import models
from Order.models import Item
from Authentication.models import User
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(
        Item, through="CartItems", related_name="cart_items")


class CartItems(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='item_in_cart')
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_no')
    quantity = models.IntegerField(default=1)

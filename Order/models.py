from django.db import models
from Authentication.models import User
from django.core.validators import MinValueValidator
# Create your models here.


class Item(models.Model):
    status_choices = [('active', 'Active'),
                      ('retire', 'Retire')]
    title = models.CharField(
        max_length=250, unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField(default=1,
                                        validators=[MinValueValidator(1)])
    status = models.CharField(max_length=50, choices=status_choices)
    photo_url = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    status_choices = [('completed', 'Completed'),
                      ('placed',
                       'Placed'), ('paid', 'Paid'),
                      ('canceled', 'Canceled')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    total_price = models.IntegerField(default=2000)
    items = models.ManyToManyField(
        Item, through='ItemOrder', related_name='ordereditems')
    status = models.CharField(
        max_length=50, choices=status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ItemOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Category(models.Model):
    Name = models.CharField(max_length=100, unique=True)
    items = models.ManyToManyField(Item, related_name='items')

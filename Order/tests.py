from django.test import TestCase
from .models import Item, Category, Order
from Authentication.models import User
import datetime
from django.urls import reverse
import pdb
# Create your tests here.


class ItemModelTests(TestCase):
    def setUp(self):
        item1 = Item.objects.create(title="Chinese Rice", description="Good",
                                    price=10,
                                    status="active", photo_url="")
        category1 = Category.objects.create(Name="Rice")
        category1.items.add(item1)

    def test_item_price_greater_than_zero(self):
        """
        An item can not have price less than 1$
        """
        item = Item.objects.create(title="Rice", description="Rice",
                                   price=0,
                                   status="active", photo_url="")
        self.assertEquals(item.price, 0)

    def test_item_title_unique(self):
        item1 = Item.objects.get(pk=1)
        item2 = Item.objects.create(title="Mutton", description="handi",
                                    price=10,
                                    status="active", photo_url="")
        # checks if title is unique
        self.assertNotEqual(item1.title, item2.title)

    def test_title_not_null(self):
        item1 = Item.objects.get(pk=1)
        self.assertNotEqual(item1.title, None)
        self.assertNotEqual(item1.title, "")

    def test_description_not_null(self):
        item1 = Item.objects.get(pk=1)
        self.assertNotEqual(item1.description, None)
        self.assertNotEqual(item1.description, "")

    def test_category_contain_one_atleast_item(self):
        category1 = Category.objects.get(pk=1)
        items = category1.items.all()
        number = len(items)
        self.assertNotEqual(number, 0)


class OrderModelTests(TestCase):
    def setUp(self):
        item1 = Item.objects.create(title="Chinese Rice", description="Good",
                                    price=10,
                                    status="active", photo_url="")
        user1 = User.objects.create(username="ali", email="ali@devsinc.com",
                                    password='ali1234', last_name='asdasdasd')
        order1 = Order.objects.create(user=user1,
                                      date_time=datetime.datetime.now(),
                                      total_price=1000, status='placed')
        order1.items.add(item1)

    def test_order_belongs_to_user(self):
        order1 = Order.objects.get(pk=1)
        self.assertIsInstance(order1.user, User)

    def order_is_for_morethan_one_items(self):
        order1 = Order.objects.get(pk=1)
        items = order1.items.all()
        number = len(items)
        self.assertNotEqual(number, 0)


class OrderViewTests(TestCase):
    def setUp(self):
        item1 = Item.objects.create(title="Chinese Rice", description="Good",
                                    price=10,
                                    status="active", photo_url="")
        user1 = User.objects.create(username="ali", email="ali@devsinc.com",
                                    password='ali1234', last_name='asdasdasd')
        order1 = Order.objects.create(user=user1,
                                      date_time=datetime.datetime.now(),
                                      total_price=1000, status='placed')
        order1.items.add(item1)

    def test_view_order_detail(self):
        response = self.client.get(
            reverse('vieworderdetails', kwargs={'pk': 2}))
        pdb.set_trace()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry No order exists for This id")

    def test_change_order_status(self):
        response = self.client.get(
            reverse('ChangeOrder', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry No order exists for This id")

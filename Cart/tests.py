from django.test import TestCase
from Order.models import Item
from Authentication.models import User
from .models import Cart
from django.urls import reverse
# Create your tests here.


class CartViewTests(TestCase):
    def setUp(self):
        item = Item.objects.create(title="Chinese Rice", description="Good",
                                   price=10,
                                   status="active", photo_url="")
        user = User.objects.create(username="ali", email="ali@devsinc.com",
                                   password="ali1234")
        cart = Cart.objects.create(user=user)
        cart.items.add(item)

    def test_view_cart(self):
        response = self.client.get(
            reverse('CartView'))
        self.assertEqual(response.status_code, 200)

    def test_add_item_in_cart(self):
        item = Item.objects.create(title="Mutton", description="Good",
                                   price=100,
                                   status="active", photo_url="")
        response = self.client.post(
            reverse('addtocart', kwargs={'id': item.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('addtocart', kwargs={'id': 20}))
        self.assertContains(response, 'Sorry No Item exists for this id')

    def test_remove_from_cart(self):
        response = self.client.post(
            reverse('removefromcart'))
        self.assertEqual(response.status_code, 404)

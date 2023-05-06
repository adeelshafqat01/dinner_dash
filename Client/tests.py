from django.test import TestCase
from Order.models import Item
from django.urls import reverse
# Create your tests here.


class ClientViewTests(TestCase):
    def setUp(self):
        Item.objects.create(title="Chinese Rice", description="Good",
                            price=10,
                            status="active", photo_url="")

    def test_view_item(self):
        response = self.client.get(
            reverse('viewitem', kwargs={'pk': 13}))
        self.assertEqual(response.status_code, 200)

    def test_find_item(self):
        response = self.client.get(
            reverse('finditems'))
        self.assertEqual(response.status_code, 200)

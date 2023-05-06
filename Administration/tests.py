from django.test import TestCase
from Authentication.models import User
from Order.models import Item
from django.urls import reverse
# Create your tests here.


class AdministrationViewTests(TestCase):
    def setUp(self):
        user = User.objects.create(
            username="ali", email="ali@devsinc.com", is_superuser=1)
        user.set_password('ali1234')
        user.save()
        Item.objects.create(title="Chinese Rice", description="Good",
                            price=10,
                            status="active", photo_url="")

    def test_login(self):
        self.client.login(username="ali", password="ali1234")
        response = self.client.get(
            reverse('admindashboard'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('homepage'))
        self.assertContains(response, 'Sorry You Cant Access This Page')

    def test_logout(self):
        self.client.login(username="ali", password="ali1234")
        response = self.client.get(
            reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_update_info(self):
        self.client.login(username="ali", password="ali1234")
        response = self.client.get(
            reverse('updateinfo', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('updateinfo', kwargs={'pk': 2}))
        self.assertContains(response, 'Sorry You Cant Access This Page')

    def test_modify_item(self):
        response = self.client.get(
            reverse('modifysingleitem', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('modifysingleitem', kwargs={'pk': 3}))
        self.assertContains(response, 'Item Does not exist')

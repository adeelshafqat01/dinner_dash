from django.test import TestCase
from .models import User
from django.urls import reverse
# Create your tests here.


class UserModelTests(TestCase):
    def setUp(self):
        User.objects.create(username="ali", email="ali@devsinc.com",
                            password='ali1234', last_name='asdasdasdasdasdasd')

    def test_user_email_unique(self):
        user1 = User.objects.get(pk=1)
        user2 = User.objects.create(username="ahmed",
                                    email="ahmed@devsinc.com",
                                    password='ahmed1234')
        self.assertNotEqual(user1.email, user2.email)

    def test_user_name_unique(self):
        user1 = User.objects.get(pk=1)
        user2 = User.objects.create(username="ahmed",
                                    email="ahmed@devsinc.com",
                                    password='ahmed1234')
        self.assertNotEqual(user1.username, user2.username)

    def test_user_name_not_blank(self):
        user1 = User.objects.get(pk=1)
        self.assertNotEqual(user1.username, None)
        self.assertNotEqual(user1.username, "")

    def test_user_displayname_length_constraint(self):
        user1 = User.objects.get(pk=1)
        self.assertGreaterEqual(len(user1.last_name), 2)
        self.assertLessEqual(len(user1.last_name), 32)


class AuthenticationViewTests(TestCase):
    def setUp(self):
        user = User.objects.create(username="ali", email="ali@devsinc.com")
        user.set_password('ali1234')
        user.save()

    def test_login(self):
        response = self.client.login(username="ali", password="ali1234")
        self.assertEqual(response, True)

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

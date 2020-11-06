from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class TestUserViews(TestCase):
    """
    User app views test.
    """

    def setUp(self):
        self.username = 'moi@gmail.com'
        self.password = 'moi'
        self.client = Client()
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_connection_page(self):
        """
        Getting the connection page should return a http code = 200.
        """

        response = self.client.get(reverse('connection'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='purbeurre_user/connection.html')

    def test_user_connection(self):
        """
        The connection with valid information should return a http code = 200.
        """

        response = self.client.post(reverse('connection'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='purbeurre_user/connection.html')

    def test_user_my_account(self):
        """
        Getting the user's account page when the user is connected should return a http code = 200.
        """

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('my_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='purbeurre_user/my_account.html')

    def test_user_disconnection(self):
        response = self.client.get(reverse('disconnection'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='purbeurre_core/home.html')

    def test_user_create_account(self):
        """
        Getting the create account page should return a http code = 200.
        """

        response = self.client.post(reverse('create_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='purbeurre_user/create_account.html')

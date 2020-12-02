from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.user.tokens import account_activation_token

# from apps.user.models import PBUser as User
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import time


class TestUserViews(TestCase):
    """
    User app views test.
    """

    def setUp(self):
        self.username = 'test@gmail.com'
        self.password = 'test'
        self.firstname = 'test'
        self.client = Client()
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.firstname = self.firstname
        self.user.is_active = False
        self.user.save()
        self.token = account_activation_token.make_token(self.user)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))

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

    def test_activate(self):
        """
        calling activate should return a http code = 302.
        after that, the user should be activated.
        """
        response = self.client.get(reverse('activate', kwargs={'uidb64': self.uid, 'token': self.token}))
        self.assertEqual(response.status_code, 302)
        user = User.\
            objects.get(pk=self.user.pk)
        self.assertEqual(user.is_active, True)
        self.assertTemplateUsed(template_name='purbeurre_user/my_account.html')

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, Client

from apps.user.forms import AccountForm


class TestUserForms(TestCase):
    """
    User app forms test.
    """

    def setUp(self):
        self.username = 'moi@gmail.com'
        self.password = 'moi'
        self.pwd_confirm = 'me'
        self.client = Client()
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.data = {
            'username': self.username,
            'password': self.password,
            'pwd_confirm': self.pwd_confirm
        }

    def test_user_account_form_same_username(self):
        """
        Tests if the user tries to create an account with an already used username.
        """

        self.assertRaises(ValidationError, AccountForm.clean_username, self)

    def test_user_account_form_wrong_confirm_pwd(self):
        """
        Tests if the confirmation password is different from the first password.
        """

        self.assertRaises(ValidationError, AccountForm.clean_pwd_confirm, self)

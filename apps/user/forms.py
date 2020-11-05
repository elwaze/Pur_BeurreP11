from django import forms

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ConnectionForm(forms.Form):
    # Form for connection.
    username = forms.EmailField(label="Identifiant : e-mail")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class AccountForm(ConnectionForm):
    # Form to create a new account.
    pwd_confirm = forms.CharField(label="Confirmation mot de passe", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Prénom", max_length=30)

    def clean_username(self):
        # Checking username validity.
        if User.objects.filter(username=self.data['username']).exists():
            raise ValidationError("Ce nom d'utilisateur existe déjà.")
        return self.data['username']

    def clean_pwd_confirm(self):
        # Checking that the confirmation password is the same than the first password.
        if self.data['password'] != self.data['pwd_confirm']:
            raise ValidationError("veuillez entrer un mot de passe de confirmation identique au mot de passe choisi. ")

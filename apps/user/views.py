from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import ConnectionForm, AccountForm
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def connection(request):
    """
    Connection to the user account.
    """

    error = False
    if request.method == "POST":
        form = ConnectionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Checking identification data
            user = authenticate(username=username, password=password)
            if user:
                # Connecting user
                login(request, user)
            else:
                # prompts an error
                error = True
    else:
        form = ConnectionForm()

    return render(request, 'connection.html', locals())


def my_account(request):
    """
    Getting the user's personal page.
    """

    return render(request, 'my_account.html', locals())


def disconnection(request):
    """
    Logging the user out.
    """

    logout(request)
    return render(request, 'home.html', locals())


def create_account(request):
    """
    Creating a new user account.
    Needs a username not already used.
    """

    error = False

    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            # checking form data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            # Creating user
            user = User.objects.create_user(username, username, password)
            user.first_name = first_name
            user.is_active = False
            user.save()
            # sending confirmation email
            subject = 'Finalisez la création de votre compte Pur Beurre'
            context = {
                'user': user,
                'domain': settings.SITE_LINK,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
                }
            email_content = render_to_string('confirmation_email.html', context)
            to_email = form.cleaned_data.get("username")
            email = EmailMessage(
                subject, email_content, to=[to_email]
            )
            response = email.send()
            activation = 'Veuillez confirmer votre adresse email pour valider la création de votre compte Pur Beurre'

            return render(request, 'create_account.html', locals())

        else:
            error = True
    else:
        form = AccountForm()
    return render(request, 'create_account.html', locals())


def activate(request, uidb64, token):
    """
    sets the user.is_active to true if the token is valid,
    login the user, redirects to the my_account page.
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('my_account')
    else:
        return HttpResponse('Le lien d\'activation est invalide, veuillez réessayer !')

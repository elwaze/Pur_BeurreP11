from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from apps.user.models import PBUser as User
from .forms import ConnectionForm, AccountForm


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
    print(request)
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
            user.active = False
            try:
                user.save()
            except Exception:
                return render() # error ?? error = True ?
            # sending confirmation email
            # sendConfirm(user)
            # if user:
            #     # Connecting user and redirecting to the user's account page.
            #     login(request, user)
            #     return redirect('my_account')
            # # prompts an error
            # else:
            #     error = True
    else:
        form = AccountForm()

    return render(request, 'create_account.html', locals())


def user_confirmation(request):
    token = request.GET.get('token')
    if not token:
        # error renv une p html disant qu'une erreur s'est produite, qu'il faut recommencer ? lien vers create account
        return
    users = User.objects.filter(token=token, active=False)
    if not users:
        # error renv une p html disant que la confirmation n'a pas pu avoir lieu, qu'il faut recommencer ?
        return render()
    for user in users:
        user.active = True
        user.save()
    return redirect('connection')

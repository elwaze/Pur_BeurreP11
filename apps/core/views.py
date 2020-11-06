from django.shortcuts import render


# home
def home(request):
    return render(request, 'home.html')


# legal notices
def legal_notices(request):
    return render(request, 'legal_notices.html')

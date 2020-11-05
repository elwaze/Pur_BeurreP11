from django.shortcuts import render, redirect
from apps.off.models import Product
from apps.favorites.models import Favorite


def favorites(request):
    """
    Shows the favorites saved by the user.
    """

    user = request.user
    favorites_found = Favorite.objects.filter(user__exact=user)
    favorites_saved = []
    for product in favorites_found:
        favorite_prod = Product.objects.search_favorite(product.favorite_id)
        favorites_saved.append(favorite_prod)
    return render(request, 'favorites.html', locals())


def save(request):
    """
    Saves a new product for the user in the favorites table of the DB.
    """

    product = request.GET.get('product')
    user = request.user
    Favorite.objects.save(product, user)
    return redirect('favorites')


def remove(request):
    """
    Removes a new product for the user in the favorites table of the DB.
    """

    product = request.POST.get('product')
    user = request.user
    Favorite.objects.remove(product, user)
    return redirect('favorites')

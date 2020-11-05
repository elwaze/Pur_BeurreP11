from django.shortcuts import render
from apps.off.models import Product


def results(request):
    """
    Shows the products found.
    """

    query = request.GET.get('query')
    substitutes, product = Product.objects.search(query)
    # if nothing found, product not found
    if not product:
        return render(
            request, 'prod_not_found.html', dict(query=query)
        )

    return render(request, 'results.html',
                  dict(product=product, substitutes=substitutes))


def detail(request, product_id=None):
    """
    Shows the detailed page of the product.
    """
    # detailed page of the product.
    product = Product.objects.get(id=product_id)
    return render(request, 'detail.html', dict(product=product))

from django.db import models


class ProductManager(models.Manager):

    def search(self, query):
        """
        Searches the products matching the given query.
        The first product found / with exact name will be the product.
        The other products found will be the substitutes,
        if their nutriscore is not worse than the product nutriscore.

        :param query: The query terms.

        :return substitutes, product_found: list of substitutes, product found.
        """
        substitutes = []
        product_found = None
        if query:
            # looking for the product
            products_found = self.filter(
                name__icontains=query
            )
            if products_found:
                product_found = products_found.filter(name__iexact=query).first()
                if not product_found:
                    product_found = products_found.first()
                substitutes = products_found.filter(
                    category=product_found.category,
                    nutriscore=product_found.nutriscore
                )
        return substitutes, product_found

    def search_favorite(self, product):
        favorite_prod = self.filter(id__exact=product).first()
        return favorite_prod


class Category(models.Model):
    """
    Class building categories and managing their interactions
    with other objects.
    """

    class Meta:
        verbose_name_plural = 'categories'
        app_label = 'off'

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    """
    Class building products and managing their interactions with other objects.
    """

    class Meta:
        unique_together = ('link', 'category',)

    objects = ProductManager()

    link = models.URLField(unique=True)
    name = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=1)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    img = models.URLField()
    nutrition_img = models.URLField(null=True, blank=True)

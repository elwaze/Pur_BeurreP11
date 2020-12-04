from django.db import models
from apps.off.models import Product
from django.contrib.auth.models import User


class FavoriteManager(models.Manager):
    def save(self, product, user):
        """
        Used to save a product in the user's favorites.

        :param product: product to be saved.
        :param user: authenticated user.
        """

        self.get_or_create(
            favorite_id=product,
            user_id=user.id
        )

    def remove(self, product, user):
        """
        Used to remove a product from the user's favorites.

        :param product: product to be deleted.
        :param user: authenticated user.
        """

        favorite = self.get(
            favorite_id=product,
            user_id=user.id
        )
        favorite.delete()


class Favorite(models.Model):

    class Meta:
        unique_together = ('user', 'favorite')

    objects = FavoriteManager()

    favorite = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='favorite')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)

from django.contrib.auth.models import User
from django.test import TestCase

from apps.off.models import Category
from apps.favorites.models import Favorite
from apps.favorites.models import FavoriteManager
from apps.favorites.models import Product


class TestFavorite(TestCase):
    """
    Tests favorite creation in DB.
    """

    def setUp(self):

        user = User.objects.create(username="abc@toto.fr", password="abc")
        category = Category.objects.create(name="category")
        product = Product.objects.create(
                    name="name",
                    link="http://url.com",
                    nutriscore="a".upper(),
                    category=category,
                    img="http://img.com",
                    nutrition_img=""
                )
        self.model = Favorite(user=user, favorite=product)

    def test_models_columns(self):
        self.assertIsInstance(self.model.user, User)
        self.assertIsInstance(self.model.favorite, Product)

    def test_favorite_objects(self):
        self.assertIsInstance(Favorite.objects, FavoriteManager)

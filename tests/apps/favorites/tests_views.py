from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from apps.favorites.models import Favorite
from apps.off.models import Product, Category


class TestFavoritesViews(TestCase):
    """
    Favorites app views test.
    """

    def setUp(self):
        self.username = 'moi@gmail.com'
        self.password = 'moi'
        self.client = Client()
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.category = Category.objects.create(name="category")
        self.product = Product.objects.create(
            name="name",
            link="http://url.com",
            nutriscore="a",
            category=self.category,
            img="http://img.com",
            nutrition_img=""
        )
        self.favorite = Favorite.objects.create(user=self.user, favorite=self.product)

    def test_favorites_favorites(self):
        """
        Getting the favorites page should return a http code = 200.
        """

        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('purbeurre_favorites/favorites.html')

    def test_favorites_save(self):
        """
        After having saved a product,
        it should be found in the user's favorites
        """

        response = self.client.get(reverse('save'), {'product': self.product.id})
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('purbeurre_favorites/favorites.html')
        prod_saved = Favorite.objects.first()
        self.assertEqual(prod_saved, self.favorite)

    def test_favorites_remove(self):
        """
        After having removed a product,
        it should not be found in the user's favorites
        """

        response = self.client.post(reverse('remove',), {'product': self.product.id})
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('purbeurre_favorites/favorites.html')
        self.assertNotIsInstance(
            Favorite.objects.filter(
                id=self.product.id,
                user=self.user.id
            ),
            Favorite
        )

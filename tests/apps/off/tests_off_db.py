from django.test import TestCase
import unittest.mock as mock
from apps.off.management.commands.off_db import Command
from apps.off.models import Category
from apps.off.models import Product


class TestCommand(TestCase):
    """
    Tests the update of the purbeurre DB from OpenFoodFacts API.
    """

    def setUp(self):
        self.command = Command()
        self.category, _ = Category.objects.get_or_create(name='testing category')
        self.product = {
            "name": "name",
            "link": "http://url.com",
            "nutriscore": "a",
            "category": self.category,
            "img": "http://img.com",
            "nutrition_img": 1
        }
        self.products = [
            {
                'url': self.product['link'],
                'product_name_fr': self.product['name'],
                'nutrition_grades': self.product['nutriscore'],
                'countries': "france",
                'image_url': self.product['img'],
                'image_nutrition_small_url': self.product['nutrition_img']
            }
        ]
        self.tags = [
            {
                'name': self.category.name,
                'products': 87932,
                'url': 'fake url'
            }
        ]
        i = 0
        while i < 16:
            self.tags.append(
                {
                    'name': f'{self.category.name}{i}',
                    'products': 87932,
                    'url': 'fake url'
                }
            )
            i += 1

    def _setup_mocked_response(self, response, **options):
        magic = options.pop('magic', False)
        if magic:
            mocked_response = mock.MagicMock(**options)
        else:
            mocked_response = mock.Mock(**options)
        mocked_response.json.return_value = response
        return mocked_response

    def test_sort_and_register_products(self):
        # calling function
        result = self.command.sort_and_register_products(
            self.products,
            self.category,
            nb_prod=0
        )
        # expected result
        self.assertEqual(result, 1)
        self.assertEqual(Product.objects.all().exists(), True)

    @mock.patch(
        'apps.off.management.commands.off_db.Command.sort_and_register_products')
    @mock.patch('requests.get')
    def test_get_products(
            self,
            mocked_requests_get,
            mocked_sort_and_register_products
    ):
        # mocking
        expected_result = {
            "products": self.products
        }
        mocked_response = self._setup_mocked_response(expected_result)
        mocked_requests_get.return_value = mocked_response
        mocked_sort_and_register_products.return_value = 1

        # calling function
        self.command.get_products(self.category, 'fake_url', 1)

        # expected result
        mocked_requests_get.assert_called_once_with('fake_url/1.json')
        mocked_sort_and_register_products.assert_called_once_with(
            expected_result['products'],
            self.category,
            0
        )

    @mock.patch(
        'apps.off.management.commands.off_db.Command.get_products'
    )
    def test_get_categories(self, mocked_get_products):

        # calling function
        self.command.get_categories(self.tags)

        # expected result
        self.assertEqual(mocked_get_products.call_count, 15)
        self.assertEqual(Category.objects.all().exists(), True)

    @mock.patch(
        'apps.off.management.commands.off_db.Command.get_categories'
    )
    @mock.patch('requests.get')
    def test_handle(self, mocked_requests_get, mocked_get_categories):
        # mocking
        expected_result = {
            "tags": self.tags
        }
        mocked_response = self._setup_mocked_response(expected_result)
        mocked_requests_get.return_value = mocked_response
        # calling function
        self.command.handle()

        # expected result
        mocked_requests_get.assert_called_once_with(
            'https://fr.openfoodfacts.org/categories&json=1'
        )
        mocked_get_categories.assert_called_once_with(self.tags)
        self.assertEqual(Product.objects.all().exists(), False)

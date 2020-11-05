from django.test import TestCase

from apps.off.models import Category, Product, ProductManager


class TestProduct(TestCase):
    """
    Tests product creation in DB.
    """

    def setUp(self):
        self.category = Category.objects.create(name="category")
        Product.objects.create(
            name="name",
            link="http://url.com",
            nutriscore="a",
            category=self.category,
            img="http://img.com",
            nutrition_img=""
        )

    def test_product_objects(self):
        self.assertIsInstance(Product.objects, ProductManager)

    def test_product_columns(self):
        product = Product.objects.get(name="name")
        self.assertEqual("name", product.name)
        self.assertEqual("http://url.com", product.link)
        self.assertEqual("a", product.nutriscore)
        self.assertEqual(self.category, product.category)
        self.assertEqual("http://img.com", product.img)
        self.assertEqual("", product.nutrition_img)


class TestCategory(TestCase):
    """
    Tests category creation in DB.
    """

    def setUp(self):
        self.category = Category.objects.create(name="category")
        self.model = Category(self.category)

    def test_category_objects(self):
        self.assertIsInstance(self.category, Category)

    def test_category_columns(self):
        self.assertEqual("category", self.category.name)

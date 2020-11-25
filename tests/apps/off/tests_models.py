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
            nutriscore="b",
            category=self.category,
            img="http://img.com",
            nutrition_img=""
        )
        Product.objects.create(
            name="product name",
            link="http://url2.com",
            nutriscore="a",
            category=self.category,
            img="http://img.com",
            nutrition_img=""
        )
        Product.objects.create(
            name="name product",
            link="http://url3.com",
            nutriscore="c",
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
        self.assertEqual("b", product.nutriscore)
        self.assertEqual(self.category, product.category)
        self.assertEqual("http://img.com", product.img)
        self.assertEqual("", product.nutrition_img)

    def test_search(self):
        """
        Checks that the ProductManager search function
        returns a product and substitutes with lower nutriscores
        """

        substitutes, product_found = Product.objects.search("name")
        # the test found a product
        self.assertEqual("name", product_found.name)
        self.assertEqual("http://url.com", product_found.link)
        self.assertEqual("b", product_found.nutriscore)
        self.assertEqual(self.category, product_found.category)
        self.assertEqual("http://img.com", product_found.img)
        self.assertEqual("", product_found.nutrition_img)
        # the product is not listed in substitutes
        self.assertNotIn(product_found, substitutes)
        for substitute in substitutes:
            assertion = product_found.nutriscore > substitute.nutriscore

            # the product's nutriscore is higher than the substitute's nutriscore
            self.assertTrue(assertion)


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

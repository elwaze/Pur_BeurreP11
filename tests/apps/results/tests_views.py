
from django.test import TestCase
from django.urls import reverse

from apps.off.models import Product, Category


class TestResultsViews(TestCase):
    """
    Results app views test.
    """

    def setUp(self):

        self.category = Category.objects.create(name="category")
        self.product = Product.objects.create(
            name="name",
            link="http://url.com",
            nutriscore="a",
            category=self.category,
            img="http://img.com",
            nutrition_img=""
        )

    def test_results_results(self):
        """
        Getting the results page with a valid product should return a http code = 200.
        """

        response = self.client.get(reverse('results'), {'query': 'name'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('purbeurre_results/results.html')

    def test_results_detail(self):
        """
        Getting the detail page should return a http code = 200.
        """

        response = self.client.get(reverse(
            'detail', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('purbeurre_results/detail.html')

    def test_results_prod_not_found(self):
        """
        Getting the results page with a wrong product should return a http code = 200.
        """

        response = self.client.get(reverse('results'), {'query': 'error'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('purbeurre_results/prod_not_found.html')

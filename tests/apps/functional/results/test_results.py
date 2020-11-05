from selenium.webdriver.common.keys import Keys

from tests.apps.functional.func_tests import GeneralTestCase


class ResultsTestCase(GeneralTestCase):

    def setUp(self):
        super().setUp()
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get('{}/home'.format(self.live_server_url))
        # finding the form element
        self.search = selenium.find_element_by_xpath('//input[@placeholder="Chercher"]')
        self.prod = selenium.find_element_by_xpath('//input[@placeholder="Produit"]')
        self.submit = selenium.find_element_by_xpath('//button[@type="submit"]')

    def test_search_from_navbar_ok(self):
        """
        Tests the food search from the navbar with a product known to be registered in the DB.
        """
        # Fill the form with data
        self.search.send_keys('pain')
        # submitting the form
        self.search.send_keys(Keys.ENTER)

        # check the returned result
        self.assertEqual(
            self.selenium.current_url,
            '{}/results/results?query=pain'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )
        self.assertIn('vous pouvez remplacer cet aliment par', self.selenium.page_source.lower())

    def test_search_from_navbar_prod_not_found(self):
        """
        Tests the food search from the navbar with a product known not to be registered in the DB.
        """
        # Fill the form with data
        self.search.send_keys('ftmpd654tedsgfra')
        # submitting the form
        self.search.send_keys(Keys.RETURN)

        # check the returned result
        self.assertEqual(
            self.selenium.current_url,
            '{}/results/results?query=ftmpd654tedsgfra'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )
        self.assertIn('vous pouvez effectuer une nouvelle recherche.', self.selenium.page_source.lower())

    def test_search_from_homepage_ok(self):
        """
        Tests the food search from the body with a product known to be registered in the DB.
        """
        # Fill the form with data
        self.prod.send_keys('pain')
        # submitting the form
        self.submit.click()

        # check the returned result
        self.assertEqual(
            self.selenium.current_url,
            '{}/results/results?query=pain'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )
        self.assertIn('vous pouvez remplacer cet aliment par :', self.selenium.page_source.lower())

    def test_search_from_homepage_prod_not_found(self):
        """
        Tests the food search from the body with a product known not to be registered in the DB.
        """
        # Fill the form with data
        self.prod.send_keys('ftmpd654tedsgfra')
        # submitting the form
        self.submit.click()

        # check the returned result
        self.assertEqual(
            self.selenium.current_url,
            '{}/results/results?query=ftmpd654tedsgfra'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )
        self.assertIn('vous pouvez effectuer une nouvelle recherche.', self.selenium.page_source.lower())

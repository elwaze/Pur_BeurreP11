from tests.apps.functional.func_tests import GeneralTestCase


class FavoritesTestCase(GeneralTestCase):

    def test_save_as_favorite(self):
        """
        Tests the registration of a product as user's favorite.
        """
        # Opening the link we want to test
        self.selenium.get('{}/results/results?query=pain'.format(self.live_server_url))
        # Click on "sauvegarder"
        save_product = self.selenium.find_element_by_id('save_product')
        save_product.click()

        # check the returned result
        self.assertEqual(
            self.selenium.current_url,
            '{}/favorites/favorites'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )
        self.assertIn('mes aliments sauvegardés', self.selenium.page_source.lower())

    def test_remove_from_favorites(self):
        """
        Tests the suppression of a favorite by the user.
        """
        # Opening the link we want to test
        self.selenium.get('{}/results/results?query=pain'.format(self.live_server_url))
        # Click on "sauvegarder"
        save_product = self.selenium.find_element_by_id('save_product')
        save_product.click()

        # Opening the link we want to test
        self.selenium.get('{}/favorites/favorites'.format(self.live_server_url))

        # Click on "Supprimer"
        delete_product = self.selenium.find_element_by_id('remove_favorite')
        delete_product.click()

        error = None
        try:
            self.selenium.find_element_by_id('remove_favorite')
        except Exception as err:
            error = err
        self.assertIsNotNone(error)
        self.assertIsInstance(error, Exception)

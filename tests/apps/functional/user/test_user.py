from tests.apps.functional.func_tests import USERNAME
from tests.apps.functional.func_tests import PASSWORD
from tests.apps.functional.func_tests import FIRST_NAME
from tests.apps.functional.func_tests import GeneralTestCase


class AccountTestCase(GeneralTestCase):
    login_required = False

    def setUp(self):
        super().setUp()

        self.create_url = '{}/user/create_account?'.format(self.live_server_url)
        self.connect_url = '{}/user/connection'.format(self.live_server_url)

    def account_basis(self, url):
        """
        Common settings depending on the page we want (create account or connection).

        :param url: url of the page we want.
        :return username, password, pwd_confirm, first_name, submit: form elements found.
        when using connection url, pwd_confirm and first_name not found
        -> replaced by an empty string.
        """
        # Opening the link we want to test
        self.selenium.get(url)

        # find the form element
        username = self.selenium.find_element_by_name("username")
        password = self.selenium.find_element_by_name("password")
        try:
            pwd_confirm = self.selenium.find_element_by_name("pwd_confirm")
            first_name = self.selenium.find_element_by_name("first_name")
        except:
            pwd_confirm = ""
            first_name = ""

        submit = self.selenium.find_element_by_xpath('//input[@type="submit"]')

        return username, password, pwd_confirm, first_name, submit

    def test_create_account_ok(self):
        """
        Tests the user account creation with a valid form.
        """
        username, password, pwd_confirm, first_name, submit = self.account_basis(self.create_url)

        # Fill the form with data
        username.send_keys('created_{}'.format(USERNAME))
        password.send_keys('created_{}'.format(PASSWORD))
        pwd_confirm.send_keys('created_{}'.format(PASSWORD))
        first_name.send_keys('createaccount')

        # submitting the form
        submit.click()
        # check the returned result
        self.assertEqual(
            self.selenium.current_url,
            '{}/user/my_account'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )

        # logout at the end of the test, not to be logged in for next test
        logout = self.selenium.find_element_by_xpath('//a[@href="/user/disconnection"]')
        logout.click()

    def test_create_account_diff_pwd(self):
        """
        Tests the user account creation,
        when the confirmation password is different from the first password.
        """
        username, password, pwd_confirm, first_name, submit = self.account_basis(self.create_url)

        # Fill the form with data
        username.send_keys('create_account_diff_pwd@selenium.com')
        password.send_keys('create_account_diff_pwd')
        pwd_confirm.send_keys('not_selenium_test')
        first_name.send_keys('createaccountdiffpwd')

        # submitting the form
        submit.click()

        # check the returned result
        self.assertIn('veuillez entrer un mot de passe de confirmation identique', self.selenium.page_source)

    def test_connection_wrong_pwd(self):
        """
        Tests the user connection with a wrong password.
        """
        username, password, pwd_confirm, first_name, submit = self.account_basis(self.connect_url)

        # Fill the form with data
        username.send_keys(USERNAME)
        password.send_keys('not_selenium_test')

        # submitting the form
        submit.click()

        # check the returned result
        self.assertIn('Utilisateur inconnu ou mauvais de mot de passe.', self.selenium.page_source)

    def test_connection_user_not_known(self):
        """
        Tests the user connection with a wrong password.
        """
        username, password, pwd_confirm, first_name, submit = self.account_basis(self.connect_url)

        # Fill the form with data
        username.send_keys('user_not_known@test.com')
        password.send_keys('selenium_test')

        # submitting the form
        submit.click()

        # check the returned result
        self.assertIn('Utilisateur inconnu ou mauvais de mot de passe.', self.selenium.page_source)

    def test_connection_ok(self):
        """
        Tests the user connection with a valid form.
        """
        username, password, pwd_confirm, first_name, submit = self.account_basis(self.connect_url)

        # Fill the form with data
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        # submitting the form
        submit.click()

        # check the returned result
        self.assertIn('Vous êtes connecté(e), {} !'.format(FIRST_NAME), self.selenium.page_source)
        self.assertEqual(
            self.selenium.current_url,
            '{}/user/connection'.format(self.live_server_url),
            "urlfound: " + self.selenium.current_url
        )

        # logout at the end of the test, not to be logged in for next test
        logout = self.selenium.find_element_by_xpath('//a[@href="/user/disconnection"]')
        logout.click()

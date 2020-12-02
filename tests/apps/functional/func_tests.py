import os
import json

from tests import TESTS_ROOT

from django.test import LiveServerTestCase
# from apps.user.models import PBUser as User
from django.contrib.auth.models import User

from selenium import webdriver
from seleniumlogin import force_login
from webdriver_manager.chrome import ChromeDriverManager

from apps.off.models import Category
from apps.off.models import Product

PASSWORD = 'connection'
FIRST_NAME = 'Selenium'
USERNAME = 'connect@endtest-mail.io'


class GeneralTestCase(LiveServerTestCase):
    """
    Parent class to setup the selenium tests.
    """
    selenium = None
    created_user = None
    login_required = True

    def setUp(self) -> None:
        self.setup_fixtures()
        if self.login_required:
            force_login(self.created_user, self.selenium, self.live_server_url)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setup_selenium_driver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @classmethod
    def setup_fixtures(cls):
        cls.created_user = User.objects.create_superuser(
            username=USERNAME, password=PASSWORD, first_name=FIRST_NAME
        )

        # Product fixtures are ordered to ensure there will be substitutes
        # Order matters (nutriscore)
        with open(os.path.join(TESTS_ROOT, './test_fixtures.json')) as fd:
            fixtures = json.load(fd)

        for category in fixtures:
            instance, _ = Category.objects.get_or_create(name=category['name'])
            for product in category['products']:
                _ = Product.objects.get_or_create(category=instance, **product)

    @classmethod
    def setup_selenium_driver(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1920x1480")
        options.add_argument("disable-infobars")
        options.add_argument("disable-extensions")
        options.add_argument("headless")

        cls.selenium = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        cls.selenium.implicitly_wait(10)

from time import sleep

from django.test import LiveServerTestCase
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class TestViewBase(LiveServerTestCase):
    """Base class to test users (login and setup)"""

    def setUp(self, endpoint="/admin/"):
        """Load data, setup and login in each test"""

        # Create admin user
        self.user, self.user_pass, _ = self.create_user()

        # Setup selenium
        self.endpoint = endpoint
        self.__setup_selenium__()

    def tearDown(self):
        """Close selenium"""
        try:
            self.driver.quit()
        except Exception:
            pass

    def __setup_selenium__(self):
        """Setup and open selenium browser"""

        chrome_options = Options()
        if settings.TEST_HEADLESS:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)

    def login(self, user: str = None, user_pass: str = None):
        # Use default user and password
        if not user:
            user = self.user
        if not user_pass:
            user_pass = self.user_pass

        # Load login page and get fields
        self.driver.get(f"{self.live_server_url}/login/")
        sleep(2)
        selectors_login = {
            "username": "input[name='username']",
            "password": "input[name='password']",
            "submit": "button[type='submit']",
        }
        fields_login = self.get_selenium_elems(selectors_login)

        fields_login["username"].send_keys(user)
        fields_login["password"].send_keys(user_pass)
        fields_login["submit"].click()

        # Wait after login
        sleep(3)

    def set_page(self, endpoint):
        """Set page"""
        self.driver.get(f"{self.live_server_url}{endpoint}")
        sleep(2)

    def get_selenium_elems(self, selectors: dict) -> dict[str, WebElement]:
        """Get selenium elements from selectors

        Args:
            selectors (dict): css selectors to find: name, value

        Returns:
            dict[str, WebElement]: selenium elements: name, value
        """
        fields = {}
        for key, value in selectors.items():
            try:
                fields[key] = self.driver.find_element(By.CSS_SELECTOR, value)
            except Exception:
                fields[key] = None
        return fields

    def create_user(
        self,
        username: str = "admin",
        password: str = "admin",
        email: str = "test@gmail.com",
    ) -> tuple[str, str, User]:
        """Create a new user and return it

        Args:
            username(str): name of user to create
            password(str): password of user to create
            email(str): email of user to create

        Returns:
            tuple:
                str: Username of the user created
                str: Password of the user created
                User: User created
        """

        # Create admin user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        return user.username, password, user

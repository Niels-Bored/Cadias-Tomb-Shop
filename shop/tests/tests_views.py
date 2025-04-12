from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.tests_base.tests_views import TestViewBase


class LoginViewTestCase(TestViewBase):
    """Class to test user login
    """

    def setUp(self):
        """Define url and CSS selectors
        """
        super().setUp("/login")
        self.selectors = {"logout_btn": ".logout-svg", "error_message": ".login-error"}

    def test_created_user(self):
        """Try to login user
        """
        self.login()
        elems = self.get_selenium_elems(self.selectors)

        self.assertIsNotNone(elems["logout_btn"])

    def test_not_created_user(self):
        """Try to login not created user
        """
        # Delete created user
        User.objects.all().delete()

        self.login()

        elems = self.get_selenium_elems(self.selectors)

        self.assertIsNone(elems["logout_btn"])

    def test_incorrect_credentials(self):
        """Try to login with incorrect password
        """
        # Login with wrong username
        self.login("juanito")

        elems = self.get_selenium_elems(self.selectors)

        # Validate not logout button
        self.assertIsNone(elems["logout_btn"])

        # Validate error message
        self.assertEqual(elems["error_message"].text, "Credenciales incorrectas")


class SignUpViewTestCase(TestCase):
    """Class to test user signup
    """
    def setUp(self):
        pass

    def __create_user__(self):
        """Create user for created user test case scenarios
        """
        User.objects.create_user(
            username="juanito", email="juan@gmail.com", password="12345678"
        )

    def test_new_user(self):
        """Try to create new user
        """
        url = reverse("signup") 

        data = {
            "first_name": "Juan",
            "last_name": "Pérez",
            "username": "juanito",
            "email": "juan@example.com",
            "password1": "clave12345",
            "password2": "clave12345",
        }

        response = self.client.post(url, data)

        # Verifica redirección después del registro
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # Verifica que el usuario fue creado
        self.assertTrue(User.objects.filter(username="juanito").exists())

    def test_invalid_username(self):
        """Try to create user when username is already been used 
        """
        self.__create_user__()

        url = reverse("signup")  # Asegúrate que este nombre coincida con tus urls

        data = {
            "first_name": "Juan",
            "last_name": "Pérez",
            "username": "juanito",
            "email": "juan@example.com",
            "password1": "clave12345",
            "password2": "clave12345",
        }

        response = self.client.post(url, data)

        # Verifica redirección después del registro
        self.assertEqual(response.status_code, 200)

        # Verifica que hay un mensaje de error con la clase signup-error
        self.assertContains(response, 'class="signup-error"')

        # Verifica que el usuario no fue creado
        self.assertEqual(User.objects.all().count(),1)
    
    def test_invalid_email(self):
        """Try to create user when email is already been used 
        """
        self.__create_user__()

        url = reverse("signup")  # Asegúrate que este nombre coincida con tus urls

        data = {
            "first_name": "Juan",
            "last_name": "Pérez",
            "username": "juanp",
            "email": "juan@gmail.com",
            "password1": "clave12345",
            "password2": "clave12345",
        }

        response = self.client.post(url, data)

        # Verifica redirección después del registro
        self.assertEqual(response.status_code, 200)

        # Verifica que hay un mensaje de error con la clase signup-error
        self.assertContains(response, 'class="signup-error"')

        # Verifica que el usuario no fue creado
        self.assertEqual(User.objects.all().count(),1)


class LogOutViewTestCase(TestCase):
    """Class to test user logout
    """
    def setUp(self):
        pass

    def test_session_closed():
        pass

class CartViewTestCase(TestCase):
    """Class to test user cart actions
    """
    def setUp(self):
        pass

    def test_add_product():
        pass

    def test_remove_product():
        pass

    def test_stock_not_exceeded():
        pass

    def test_stock_exceeded():
        pass

    def test_not_zero_amount():
        pass

class ShopViewTestCase(TestCase):
    """Class to test user actions on shop
    """
    def setUp(self):
        pass

    def test_stock_not_exceeded():
        pass

    def test_stock_exceeded():
        pass

class HomeViewTestCase(TestCase):
    """Class to test user actions on home
    """
    def setUp(self):
        pass

    def test_stock_not_exceeded():
        pass

    def test_stock_exceeded():
        pass

class BlogViewTestCase(TestCase):
    """Class to test user actions on blog
    """
    def setUp(self):
        pass


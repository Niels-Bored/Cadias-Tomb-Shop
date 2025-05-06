from time import sleep

from django.contrib.auth.models import User
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


from core.tests_base.tests_views import TestViewBase, TestSeleniumBase
from shop import models


class LoginViewTestCase(TestViewBase):
    """Class to test user login"""

    def setUp(self):
        """Define url and CSS selectors"""
        super().setUp("/login")
        self.selectors = {"logout_btn": ".logout-svg", "error_message": ".login-error"}

    def test_created_user(self):
        """Try to login user"""
        self.login()
        elems = self.get_selenium_elems(self.selectors)

        self.assertIsNotNone(elems["logout_btn"])

    def test_not_created_user(self):
        """Try to login not created user"""
        # Delete created user
        User.objects.all().delete()

        self.login()

        elems = self.get_selenium_elems(self.selectors)

        self.assertIsNone(elems["logout_btn"])

    def test_incorrect_credentials(self):
        """Try to login with incorrect password"""
        # Login with wrong username
        self.login("juanito")

        elems = self.get_selenium_elems(self.selectors)

        # Validate not logout button
        self.assertIsNone(elems["logout_btn"])

        # Validate error message
        self.assertEqual(elems["error_message"].text, "Credenciales incorrectas")


class SignUpViewTestCase(TestCase):
    """Class to test user signup"""

    def setUp(self):
        pass

    def __create_user__(self):
        """Create user for created user test case scenarios"""
        User.objects.create_user(
            username="juanito", email="juan@gmail.com", password="12345678"
        )

    def test_new_user(self):
        """Try to create new user"""
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
        """Try to create user when username is already been used"""
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
        self.assertEqual(User.objects.all().count(), 1)

    def test_invalid_email(self):
        """Try to create user when email is already been used"""
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
        self.assertEqual(User.objects.all().count(), 1)


class LogOutViewTestCase(TestCase):
    """Class to test user logout"""

    def setUp(self):
        pass

    def test_session_closed():
        pass


class ShopViewTestCase(TestCase):
    """Class to test user actions on shop"""

    def setUp(self):
        pass

    def test_stock_not_exceeded():
        pass

    def test_stock_exceeded():
        pass


class HomeViewTestCase(TestCase):
    """Class to test user actions on home"""

    def setUp(self):
        pass

    def test_stock_not_exceeded():
        pass

    def test_stock_exceeded():
        pass


class BlogViewTestCase(TestCase):
    """Class to test user actions on blog"""

    def setUp(self):
        pass

class CartViewTestCase(TestSeleniumBase):
    """Class to test user cart actions"""

    def setUp(self):
        super().setUp("/cart/")

        # Create data
        self.product = models.Producto.objects.create(
            nombre="Stompa",
            imagen="https://www.warhammer.com/app/resources/catalog/product/920x950/99120103021_StompaNEW01.jpg?fm=webp&w=920&h=948",
            precio=3000,
            marca="Games Workshop",
            stock=5,
        )

        # Test variables
        self.selectors = {
            "add_btn": "a.product-item span"
        }

    def tearDown(self):
        """Close selenium"""
        try:
            self.driver.quit()
        except Exception:
            pass
    
    def add_product(self):
        """
        Add product to cart
        """
        selectors = {
            "alert_title": "#swal2-title"
        }

        # load product page
        self.set_page("/shop/1")
        
        # Click to add product with js
        self.click_js(selector=self.selectors["add_btn"])
        sleep(3)
        
        # Validate alert text
        elems = self.get_selenium_elems(selectors)
        self.assertIn("Producto añadido", elems["alert_title"].text)

    def test_add_product_logged(self):
        """
        Try to add a product on cart logged.
        Expected: update localstorage
        """

        selectors = {
            "cart_product": "td.product-name"
        }

        # add product to cart
        self.add_product()

        # load cart page
        self.set_page("/cart/")

        elems = self.get_selenium_elems(selectors)
        self.assertIn("Stompa", elems["cart_product"].text)

    
    def test_remove_product(self):
        """
        Try to add a product on cart logged.
        Expected: update localstorage
        """

        selectors = {
            "cart_product": "td.product-name",
            "btn_delete": "button.delete"
        }

        # add product to cart
        self.add_product()

        # load cart page
        self.set_page("/cart/")

        # validate product was added
        elems = self.get_selenium_elems(selectors)
        self.assertIn("Stompa", elems["cart_product"].text)
        
        # delete product
        self.click_js(selector=selectors["btn_delete"])
        sleep(3)
        elems = self.get_selenium_elems(selectors)
        if elems["cart_product"]:
            self.assertNotIn("Stompa", elems["cart_product"].text)
        else:
            self.assertNotIn("Stompa", "")
    
    def test_stock_not_exceeded(self):
        """
        Try to add products when stock is not exceeded
        """

        selectors = {
            "product_qty": "input.quantity-amount",
            "btn_add": "button.increase"
        }

        # add product to cart
        self.add_product()

        # load cart page
        self.set_page("/cart/")

        # validate product was added
        elems = self.get_selenium_elems(selectors)
        self.assertIn("1", elems["product_qty"].get_attribute('value'))
        
        # add product
        self.click_js(selector=selectors["btn_add"])
        sleep(3)

        # validate product quantity was increased
        elems = self.get_selenium_elems(selectors)
        self.assertIn("2", elems["product_qty"].get_attribute('value'))
        

    def test_stock_exceeded(self):
        """
        Try to add products when stock is not exceeded
        """

        selectors = {
            "product_qty": "input.quantity-amount",
            "btn_add": "button.increase"
        }

        # set stock
        self.product.reduce_stock(3)

        # add product to cart
        self.add_product()

        # load cart page
        self.set_page("/cart/")

        # validate product was added
        elems = self.get_selenium_elems(selectors)
        self.assertIn("1", elems["product_qty"].get_attribute('value'))
        
        # add product
        self.click_js(selector=selectors["btn_add"])
        sleep(3)

        # validate product was added
        elems = self.get_selenium_elems(selectors)
        self.assertIn("2", elems["product_qty"].get_attribute('value'))
        
        # add product
        self.click_js(selector=selectors["btn_add"])
        sleep(3)

        # validate product quantity was increased
        elems = self.get_selenium_elems(selectors)
        self.assertNotIn("3", elems["product_qty"].get_attribute('value'))

class SaleViewTestCase(TestSeleniumBase):
    """Class to test user sale actions"""

    def setUp(self):
        super().setUp("/cart/")

        # Create data
        self.product = models.Producto.objects.create(
            nombre="Stompa",
            imagen="https://www.warhammer.com/app/resources/catalog/product/920x950/99120103021_StompaNEW01.jpg?fm=webp&w=920&h=948",
            precio=3000,
            marca="Games Workshop",
            stock=5,
        )

        # Test variables
        self.selectors = {
            "add_btn": "a.product-item span",
            "btn_buy": ".btn-buy"
        }

    def tearDown(self):
        """Close selenium"""
        try:
            self.driver.quit()
        except Exception:
            pass

    
    def add_product(self):
        """
        Add product to cart
        """
        selectors = {
            "alert_title": "#swal2-title"
        }

        # load product page
        self.set_page("/shop/1")
        
        # Click to add product with js
        self.click_js(selector=self.selectors["add_btn"])
        sleep(3)
        
        # Validate alert text
        elems = self.get_selenium_elems(selectors)
        self.assertIn("Producto añadido", elems["alert_title"].text)

    def test_buy_product_logged(self):
        """
        Try to buy a product on cart logged.
        Expected: redirect to stripe
        """

        selectors = {}

        # add product to cart
        self.add_product()

        # load cart page
        self.set_page("/cart/")

        # click on buy button
        self.click_js(selector=self.selectors["btn_buy"])
        sleep(3)

        # Validate redirect to stripe
        self.assertIn("stripe", self.driver.current_url)

    def test_buy_product_without_login(self):
        """
        Try to buy a product on cart without login.
        Expected: redirect to login
        """

        selectors = {
            "btn_logout":"a.logout-svg"
        }

        # add product to cart
        self.add_product()

        self.click_js(selector=selectors["btn_logout"])
        sleep(1)

        # load cart page
        self.set_page("/cart/")

        # click on buy button
        self.click_js(selector=self.selectors["btn_buy"])
        sleep(3)

        # validate redirect to login
        self.assertIn("login", self.driver.current_url)

    def test_buy_product_stock_exceeded(self):
        """
        Try to buy a product on cart when the stock is reduce .
        Expected: redirect to stripe
        """

        selectors = {
            "alert_title": "#swal2-title",
            "cart_product": "td.product-name"
        }

        # add product to cart
        self.add_product()

        # load cart page
        self.set_page("/cart/")

        # set stock
        self.product.reduce_stock(5)

        # click on buy button
        self.click_js(selector=self.selectors["btn_buy"])
        sleep(3)

        # validate alert text
        elems = self.get_selenium_elems(selectors)
        self.assertIn("Stock insuficiente", elems["alert_title"].text)

        # validate product removed
        self.set_page("/cart/")
        elems = self.get_selenium_elems(selectors)
        if elems["cart_product"]:
            self.assertNotIn("Stompa", elems["cart_product"].text)
        else:
            self.assertNotIn("Stompa", "")

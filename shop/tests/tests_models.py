from django.test import TestCase
from shop import models

class ProductoTestCase(TestCase):
    def setUp(self):
        """Create test product
        """
        self.producto = models.Producto.objects.create(
            nombre="Stompa", 
            url_imagen="sample.com",
            precio=3000,
            marca="Games Workshop",
            stock=2
        )

    def test_reduce_stock_greater_than(self):
        """Try to reduce stock when stock is greater than amount
        """

        result = self.producto.reduce_stock(1)

        self.assertTrue(result)

    def test_reduce_stock_equal_than(self):
        """Try to reduce stock when stock is equal than  amount
        """
        result = self.producto.reduce_stock(2)

        self.assertTrue(result)

    def test_reduce_stock_lower_than(self):
        """Try to reduce stock when stock is equal than  amount
        """
        result = self.producto.reduce_stock(3)

        self.assertFalse(result)

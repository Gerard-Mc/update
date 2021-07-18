from django.test import TestCase
from .models import Product, Category


class ProductTests(TestCase):

    def test_name(self):
        test_name = Product(name='Test product')
        self.assertEqual(str(test_name), 'Test product')


class CategoryTests(TestCase):

    def test_name(self):
        test_name = Category(name='Test name')
        self.assertEqual(str(test_name), 'Test name')

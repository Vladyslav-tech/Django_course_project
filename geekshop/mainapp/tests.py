from django.test import TestCase
from django.test.client import Client
from mainapp.models import ProductCategory, Product


class TestMainappSmoke(TestCase):
    def setUp(self):
        self.client = Client()
        category = ProductCategory.objects.create(name="стулья")
        self.product_1 = Product.objects.create(name="стул 1",
                                                category=category,
                                                price=1999.5,
                                                quantity=150)

        self.product_2 = Product.objects.create(name="стул 2",
                                                category=category,
                                                price=2998.1,
                                                quantity=125,
                                                is_active=False)

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_contact_us_url(self):
        response = self.client.get('/contact_us/')
        self.assertEqual(response.status_code, 200)

    def test_products_url(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_products_category_url(self):
        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, 200)

    def test_product_category_pk_urls(self):
        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, 200)

    def test_product_details_urls(self):
        for product in Product.objects.all():
            response = self.client.get(f'/products/product_details/{product.pk}/')
            self.assertEqual(response.status_code, 200)

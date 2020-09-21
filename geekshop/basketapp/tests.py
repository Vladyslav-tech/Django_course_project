from django.test import TestCase, Client

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from basketapp.models import Basket


class TestBasketappSmoke(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="стулья")
        self.user = ShopUser.objects.create_user('tarantino', \
                                                 'tarantino@geekshop.local', 'geekbrains')

        product_1 = Product.objects.create(name="стул 1",
                                           category=category,
                                           price=1999.5,
                                           quantity=150)

        product_2 = Product.objects.create(name="стул 2",
                                                category=category,
                                                price=2998.1,
                                                quantity=125,
                                                is_active=False)
        product_3 = Product.objects.create(name="стул 3",
                                                category=category,
                                                price=998.1,
                                                quantity=115)
        self.basket_1 = Basket.objects.create(user=self.user, product=product_1, quantity=3)
        self.basket_2 = Basket.objects.create(user=self.user, product=product_2, quantity=6)
        self.basket_3 = Basket.objects.create(user=self.user, product=product_3, quantity=4)


    def test_product_cost(self):
        self.assertEqual((self.basket_1.product.price * self.basket_1.quantity), 5998.5)

    def test_total_quantity(self):
        "return total quantity for user"
        items = Basket.objects.filter(user=self.user)
        totalquantity = sum(list(map(lambda x: x.quantity, items)))
        self.assertEqual(totalquantity, 13)
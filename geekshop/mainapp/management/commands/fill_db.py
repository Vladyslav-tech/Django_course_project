from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser

import json, os

JSON_PATH = 'mainapp/json'

def load_from_file(file):
    with open(os.path.join(JSON_PATH, file + '.json'), 'r') as data:
        return json.load(data)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_file('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_file('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product["category"]
            # Получаем категорию по имени
            _category = ProductCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        super_user = ShopUser.objects.create_superuser(
            'django',
            'django@geekshop.local',
            'geekbrains',
            age=30
        )
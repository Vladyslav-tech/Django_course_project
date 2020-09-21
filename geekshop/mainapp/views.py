from django.shortcuts import render
import json
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

from .models import ProductCategory, Product
from basketapp.models import Basket

def main(request):
   title = 'главная'

   products = Product.objects.\
                      filter(is_active=True, category__is_active=True).\
                      select_related('category')[:4]

   trending_product = [
               {'scr': "/static/img/product-11.jpg", 'name': 'product-11'},
               {'scr': "/static/img/product-21.jpg", 'name': 'product-21'},
               {'scr': "/static/img/product-31.jpg", 'name': 'product-31'},
               {'scr': "/static/img/product-41.jpg", 'name': 'product-41'},
               {'scr': "/static/img/product-51.jpg", 'name': 'product-51'},
               {'scr': "/static/img/product-61.jpg", 'name': 'product-61'}
           ]
   exclusive_product = [
       {'scr': '/static/img/product-2-sm.jpg', 'name': 'product-2-sm'},
       {'scr': '/static/img/product-3-sm.jpg', 'name': 'product-3-sm'},
       {'scr': '/static/img/product-4-sm.jpg', 'name': 'product-4-sm'},
       {'scr': '/static/img/product-5-sm.jpg', 'name': 'product-5-sm'}
   ]

   context = {
       'title': title,
       'products': products,
       'exclusive_product': exclusive_product,
       'trending_product': trending_product,
   }

   return render(request, 'mainapp/index.html', context)

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []

def get_hot_product():
    products = Product.objects.filter(is_active=True, category__is_active=True,
                                      quantity__gte=1).select_related()
    return random.choice(products)


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category,
                                           is_active=True).exclude(pk=hot_product.pk)[:2]
    return same_products


def product(request, pk=None, page=1):
    title = 'продукты'
    submenu = ProductCategory.objects.filter(is_active=True)
    basket = get_basket(request.user)

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            category = {'pk': 0,
                        'name': 'все'
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True,
                                              category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': 'products',
            'submenu': submenu,
            'category': category,
            'products': products_paginator,
        }

        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'title': title,
        'submenu': submenu,
        'hot_product': hot_product,
        'same_products': same_products
    }
    return render(request, 'mainapp/product.html', context=context)

def product_details(request, pk):
    submenu = ProductCategory.objects.filter(is_active=True)
    product = get_object_or_404(Product, pk=pk)
    same_products = get_same_products(product)
    context = {
        'title': 'Product Details',
        'submenu': submenu,
        'product': product,
        'same_products': same_products
    }
    return render(request, 'mainapp/product_details.html', context=context)

def contact_us(request):
    with open("mainapp/json/contact.json", "r") as file:
        contact_data = json.load(file)

    context = {
        'title': 'Contuct Us',
        'contact_data': contact_data
    }
    return render(request, 'mainapp/contact_us.html', context=context)
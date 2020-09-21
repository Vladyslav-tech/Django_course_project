from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.product, name='products'),
    path('product_details/<int:pk>/', mainapp.product_details, name='product_details'),
    path('category/<int:pk>/page/<int:page>/', mainapp.product, name='page'),
    path('category/<int:pk>/', mainapp.product, name='category')
]
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),  # для AJAX-запросов
    path('decrement/<int:product_id>/', views.cart_decrement, name='cart_decrement'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('status/', views.cart_status, name='cart_status'),
]

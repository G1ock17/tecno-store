from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]

urlpatterns += [
    path('order/create/', views.order_create, name='order_create'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/success/', views.order_success, name='order_success'),
]
urlpatterns += [
    path('search/', views.product_search, name='product_search'),
    path('api/live-search/', views.live_search_api, name='live_search_api'),
]
urlpatterns += [
    path('privacy_policy/', views.privacy_policy, name='public_offer'),
    path('public_offer/', views.public_offer, name='public_offer'),
    path('delivery_and_payment/', views.delivery_and_payment, name='public_offer'),
]
from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product  # замените на свою модель продукта
from .cart import Cart
from django.http import JsonResponse


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'count': cart.__len__(),
            'total': cart.get_total_price()
        })
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Возвращаем только содержимое корзины для AJAX
        return render(request, 'cart/_cart_content.html', {'cart': cart})
    # Полная страница для прямого доступа
    return render(request, 'cart/detail.html', {'cart': cart})


# Удаление товара из корзины
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'count': cart.get_total_quantity()})
    else:
        return redirect('cart:cart_detail')


def cart_status(request):
    cart = Cart(request)
    return JsonResponse({
        'count': cart.get_total_quantity(),
        'total_price': float(cart.get_total_price())  # если нужно
    })

def cart_decrement(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrement(product)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'count': cart.get_total_quantity()})
    return redirect('cart:cart_detail')

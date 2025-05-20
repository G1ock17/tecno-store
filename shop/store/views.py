from django.shortcuts import render, get_object_or_404
from .models import ContactsMessage, Category, Order, OrderItem, Product, Attribute, ProductAttribute, AttributeValue
from django.shortcuts import redirect
from cart.cart import Cart
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render
from django.core.paginator import Paginator


def home(request):
    return render(request, 'store/home.html')


def get_cart(request):
    # Пример функции, которая извлекает данные корзины из сессии
    cart = request.session.get('cart', {})
    return cart


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        # Обработка данных формы заказа
        order = Order.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            postal_code=request.POST.get('postal_code'),
            city=request.POST.get('city'),
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()
        messages.success(request, 'Ваш заказ успешно оформлен!')
        return redirect('store:order_success')  # Перенаправление на страницу успеха

    return render(request, 'orders/order_create.html', {'cart': cart})


def order_success(request):
    return render(request, 'orders/order_success.html')


# views.py
def contacts(request):
    if request.method == 'POST':
        # Обработка данных формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')

        # Сохранение в базу данных
        ContactsMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        # Редирект с сообщением об успехе
        messages.success(request, 'Ваше сообщение успешно отправлено!')
        return redirect('store:contacts')

    # GET-запрос - просто отображаем форму
    return render(request, 'store/contacts.html')


# def product_list(request):
#     products = Product.objects.filter(available=True)
#     return render(request, 'store/product_list.html', {'products': products})


def product_list(request):
    products = Product.objects.filter(available=True) \
        .select_related('category') \
        .prefetch_related('images') \
        .order_by('-created')

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    try:
        min_price = request.GET.get('min_price')
        if min_price:
            products = products.filter(price__gte=float(min_price))

        max_price = request.GET.get('max_price')
        if max_price:
            products = products.filter(price__lte=float(max_price))
    except (ValueError, TypeError):
        pass

    if hasattr(Product, 'attributes'):
        attributes = request.GET.getlist('attr')
        if attributes:
            query = Q()
            for attr in attributes:
                try:
                    attr_id, value_id = attr.split('_')
                    query |= Q(attributes__attribute_id=attr_id,
                               attributes__value_id=value_id)
                except (ValueError, IndexError):
                    continue
            if query:
                products = products.filter(query).distinct()

    # 4. Сортировка (проверяем допустимые значения)
    sort_options = {'price', '-price', '-created', 'created'}
    sort = request.GET.get('sort', '-created')
    if sort in sort_options:
        products = products.order_by(sort)

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'attrvalues': AttributeValue.objects.all(),
        'attributes': Attribute.objects.all() if hasattr(Product, 'attributes') else [],
    }
    return render(request, 'store/product_list.html', context)


def get_subcategories(request):
    parent_id = request.GET.get('parent_id')
    if parent_id:
        subcategories = Category.objects.filter(parent_id=parent_id).values('id', 'name')
        return JsonResponse({'subcategories': list(subcategories)})
    return JsonResponse({'subcategories': []})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'store/product_detail.html', {'product': product})


def cart_add(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})


def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    ) if query else Product.objects.none()

    return render(request, 'store/product_list.html', {
        'products': products,
        'search_query': query
    })


def live_search_api(request):
    query = request.GET.get('q', '')
    if len(query) >= 2:  # Ищем только при вводе 2+ символов
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )[:5]  # Ограничиваем 5 результатами

        results = {
            'products': [
                {
                    'id': p.id,
                    'name': p.name,
                    'slug': p.slug,
                    'price': str(p.price),
                    'image': p.image.url if p.image else '/static/images/no-image.png'
                } for p in products
            ]
        }
        return JsonResponse(results)
    return JsonResponse({'products': []})


def privacy_policy(request):
    return render(request, 'store/privacy_policy.html')


def public_offer(request):
    return render(request, 'store/public_offer.html')


def delivery_and_payment(request):
    return render(request, 'store/delivery_and_payment.html')

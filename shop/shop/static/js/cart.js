const cartContainer = document.getElementById('cart-container');
const CART_URLS = {
  detail: cartContainer.dataset.cartDetailUrl,
  add: cartContainer.dataset.cartAddUrl
};

// Обновление содержимого корзины
function refreshCartSidebar() {
    fetch(CART_URLS.detail, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.text())
    .then(html => {
        document.querySelector('.cart-sidebar-content').innerHTML = html;
    });
}

// Делегирование событий на +, -, удалить
document.body.addEventListener('click', function(e) {
    const target = e.target.closest('[data-url]');
    if (!target) return;

    const isCartAction = target.classList.contains('cart-increment') ||
                         target.classList.contains('cart-decrement') ||
                         target.classList.contains('cart-remove') ||
                         target.classList.contains('add-to-cart');

    if (isCartAction) {
        e.preventDefault();
        const url = target.dataset.url;
        if (!url) return;

        fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
            cartFunctions.updateCartCount(data.count);
            cartFunctions.animateCartAdd();
            refreshCartSidebar();
        });
    }
});


// Делегирование событий на + и -
document.addEventListener('DOMContentLoaded', function() {
    refreshCartSidebar();
    updateCartStatus();

    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.querySelector('.cart-overlay');
    const cartCloseBtn = document.querySelector('.cart-close-btn');
    const cartToggles = document.querySelectorAll('.cart-toggle');

    // Открытие/закрытие корзины
    function toggleCart() {
        cartSidebar.classList.toggle('active');
        cartOverlay.classList.toggle('active');
        document.body.classList.toggle('no-scroll');
    }

    // Обработчики кнопок открытия/закрытия
    cartToggles.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            toggleCart();
        });
    });
    cartCloseBtn.addEventListener('click', toggleCart);
    cartOverlay.addEventListener('click', toggleCart);

    // Обновление счётчика товаров в иконке корзины
    function updateCartCount(count) {
        const cartCount = document.querySelector('.cart-count');
        const cartIcon = document.querySelector('.cart-icon');

        if (count > 0) {
            if (!cartCount) {
                cartIcon.innerHTML += `<span class="cart-count">${count}</span>`;
            } else {
                cartCount.textContent = count;
            }
        } else if (cartCount) {
            cartCount.remove();
        }
    }

    function updateCartStatus() {
    fetch('/cart/status/', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        cartFunctions.updateCartCount(data.count); // обновляем счетчик
        // можно дополнить выводом total_price, если нужно
    })
    .catch(error => console.error('Ошибка при получении статуса корзины:', error));
}

    // Анимация иконки корзины
    function animateCartAdd() {
        const cartIcon = document.querySelector('.cart-icon');
        cartIcon.classList.add('animate-bounce');
        setTimeout(() => cartIcon.classList.remove('animate-bounce'), 1000);
    }

    // Экспорт функций
    window.cartFunctions = {
        updateCartCount,
        animateCartAdd,
        toggleCart
    };
});

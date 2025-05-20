document.addEventListener('DOMContentLoaded', function() {
    // Плавный скролл
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Удаление анимаций после загрузки
    setTimeout(function() {
        document.querySelectorAll('.animate__animated').forEach(el => {
            el.classList.remove('animate__animated');
        });
    }, 1000);

    // Инициализация корзины
    if (typeof cartFunctions !== 'undefined') {
        // Можно вызвать cartFunctions.updateCartCount(5) для теста
    }
});
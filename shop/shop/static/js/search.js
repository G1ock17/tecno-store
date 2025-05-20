document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('liveSearchInput');
    const searchResults = document.getElementById('searchResults');
    let searchTimeout;

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();

        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }

        // Показываем индикатор загрузки
        searchResults.innerHTML = '<div class="text-center py-3"><i class="fas fa-spinner fa-spin"></i></div>';
        searchResults.style.display = 'block';

        searchTimeout = setTimeout(() => {
            fetch(`/api/live-search/?q=${encodeURIComponent(query)}`)
                .then(response => {
                    if (!response.ok) throw new Error('Network error');
                    return response.json();
                })
                .then(data => {
                    if (data.products && data.products.length > 0) {
                        let html = '';
                        data.products.forEach(product => {
                            html += `
                            <a href="/product/${product.slug}/" class="search-result-item">
                                <img src="${product.image}" alt="${product.name}" class="search-result-img">
                                <div class="search-result-content">
                                    <div class="search-result-title">${product.name}</div>
                                    <div class="search-result-price">${product.price} ₽</div>
                                </div>
                                </div>
                            </a>`;
                        });
                        searchResults.innerHTML = html;
                    } else {
                        searchResults.innerHTML = '<div class="no-results">Ничего не найдено</div>';
                    }
                    searchResults.style.display = 'block';
                })
                .catch(error => {
                    console.error('Ошибка поиска:', error);
                    searchResults.innerHTML = '<div class="no-results">Ошибка загрузки</div>';
                    searchResults.style.display = 'block';
                });
        }, 300); // Задержка 300мс
    });

    // Скрываем результаты при клике вне поиска
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
});
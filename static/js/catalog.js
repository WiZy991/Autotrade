// Catalog pagination with "Load More" button
document.addEventListener('DOMContentLoaded', function() {
    const loadMoreBtn = document.getElementById('load-more-btn');
    const carsGrid = document.getElementById('cars-grid');
    const loadingSpinner = document.getElementById('loading-spinner');
    
    if (!loadMoreBtn || !carsGrid) return;
    
    loadMoreBtn.addEventListener('click', function() {
        const page = parseInt(this.getAttribute('data-page'));
        const country = this.getAttribute('data-country');
        const type = this.getAttribute('data-type');
        const search = this.getAttribute('data-search');
        
        // Показываем спиннер, скрываем кнопку
        loadMoreBtn.style.display = 'none';
        loadingSpinner.style.display = 'block';
        
        // Формируем URL с параметрами
        const url = new URL('/catalog/load-more/', window.location.origin);
        url.searchParams.set('page', page);
        if (country) url.searchParams.set('country', country);
        if (type) url.searchParams.set('type', type);
        if (search) url.searchParams.set('search', search);
        
        // AJAX запрос
        fetch(url.toString(), {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.html) {
                // Создаем временный контейнер для парсинга HTML
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = data.html;
                
                // Добавляем новые карточки в сетку
                const newCards = tempDiv.querySelectorAll('.car-card');
                newCards.forEach(card => {
                    carsGrid.appendChild(card);
                });
                
                // Форматируем цены в новых карточках
                const newPriceElements = tempDiv.querySelectorAll('.car-price');
                newPriceElements.forEach(priceElement => {
                    formatPrice(priceElement);
                });
                
                // Обновляем состояние кнопки
                if (data.has_more) {
                    loadMoreBtn.setAttribute('data-page', data.page);
                    loadMoreBtn.style.display = 'inline-block';
                } else {
                    // Если больше нет машин, скрываем контейнер кнопки
                    const loadMoreContainer = loadMoreBtn.closest('.load-more-container');
                    if (loadMoreContainer) {
                        loadMoreContainer.style.display = 'none';
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error loading more cars:', error);
            loadMoreBtn.style.display = 'inline-block';
            alert('Произошла ошибка при загрузке. Попробуйте ещё раз.');
        })
        .finally(() => {
            loadingSpinner.style.display = 'none';
        });
    });
    
    // Функция форматирования цены (из main.js)
    function formatPrice(priceElement) {
        const text = priceElement.textContent || priceElement.innerText;
        const match = text.match(/(\d+)\s*₽/);
        if (match) {
            const number = parseInt(match[1]);
            const formatted = number.toLocaleString('ru-RU').replace(/,/g, ' ');
            priceElement.textContent = formatted + ' ₽';
        }
    }
});


// Галерея изображений в полный экран
document.addEventListener('DOMContentLoaded', function() {
    // Создаем модальное окно
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <span class="modal-close"></span>
        <div class="modal-content">
            <span class="modal-nav prev"></span>
            <img class="modal-image" src="" alt="">
            <span class="modal-nav next"></span>
            <div class="modal-counter"></div>
        </div>
    `;
    document.body.appendChild(modal);

    const modalImage = modal.querySelector('.modal-image');
    const modalClose = modal.querySelector('.modal-close');
    const modalPrev = modal.querySelector('.modal-nav.prev');
    const modalNext = modal.querySelector('.modal-nav.next');
    const modalCounter = modal.querySelector('.modal-counter');

    let currentImages = [];
    let currentIndex = 0;

    // Функция открытия модального окна
    function openModal(images, startIndex = 0) {
        currentImages = images;
        currentIndex = startIndex;
        modal.classList.add('active');
        updateModalImage();
        document.body.style.overflow = 'hidden';
    }

    // Функция закрытия модального окна
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Обновление изображения в модальном окне
    function updateModalImage() {
        if (currentImages.length > 0) {
            modalImage.src = currentImages[currentIndex].src;
            modalImage.alt = currentImages[currentIndex].alt || '';
            modalCounter.textContent = `${currentIndex + 1} / ${currentImages.length}`;
        }
    }

    // Переключение изображений
    function nextImage() {
        if (currentImages.length > 0) {
            currentIndex = (currentIndex + 1) % currentImages.length;
            updateModalImage();
        }
    }

    function prevImage() {
        if (currentImages.length > 0) {
            currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
            updateModalImage();
        }
    }

    // Обработчики событий
    modalClose.addEventListener('click', closeModal);
    modalNext.addEventListener('click', nextImage);
    modalPrev.addEventListener('click', prevImage);

    // Закрытие по клику на фон
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Навигация клавиатурой
    document.addEventListener('keydown', function(e) {
        if (modal.classList.contains('active')) {
            if (e.key === 'Escape') {
                closeModal();
            } else if (e.key === 'ArrowRight') {
                nextImage();
            } else if (e.key === 'ArrowLeft') {
                prevImage();
            }
        }
    });

    // Обработка кликов на изображения автомобилей ТОЛЬКО на странице деталей
    function setupImageClickHandlers() {
        // НЕ обрабатываем клики на изображения в карточках списка/каталога
        // Обрабатываем только на странице деталей автомобиля
        
        // Обработка кликов на странице деталей
        const detailHeader = document.querySelector('.car-detail-header');
        if (detailHeader) {
            const mainImg = detailHeader.querySelector('.car-detail-image img');
            if (mainImg) {
                mainImg.style.cursor = 'pointer';
                mainImg.addEventListener('click', function() {
                    // Собираем все изображения: главное + галерея
                    const allImages = [this];
                    const galleryImages = document.querySelectorAll('.car-detail-gallery img');
                    galleryImages.forEach(galleryImg => allImages.push(galleryImg));
                    openModal(allImages, 0);
                });
            }
        }
    }

    setupImageClickHandlers();

    // Обработка кликов на изображения в галерее
    document.querySelectorAll('.car-detail-gallery img').forEach(img => {
        img.classList.add('gallery-thumbnail');
        img.style.cursor = 'pointer';
        img.addEventListener('click', function() {
            // Собираем главное изображение + все из галереи
            const detailHeader = document.querySelector('.car-detail-header');
            const allImages = [];
            
            if (detailHeader) {
                const mainImg = detailHeader.querySelector('.car-detail-image img');
                if (mainImg) allImages.push(mainImg);
            }
            
            const galleryImages = document.querySelectorAll('.car-detail-gallery img');
            galleryImages.forEach(galleryImg => allImages.push(galleryImg));
            
            const startIndex = allImages.indexOf(this);
            openModal(allImages, startIndex >= 0 ? startIndex : 0);
        });
    });
});


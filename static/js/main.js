// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
        });
    });

    // Close flash messages
    const flashCloseButtons = document.querySelectorAll('.flash-close');
    flashCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const flashMessage = this.parentElement;
            flashMessage.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                flashMessage.remove();
            }, 300);
        });
    });

    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            if (message.parentElement) {
                message.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }
        }, 5000);
    });

    // Format prices with spaces (thousands separator)
    function formatPrice(priceElement) {
        const text = priceElement.textContent || priceElement.innerText;
        // Extract number and currency symbol
        const match = text.match(/(\d+)\s*₽/);
        if (match) {
            const number = parseInt(match[1]);
            const formatted = number.toLocaleString('ru-RU').replace(/,/g, ' ');
            priceElement.textContent = formatted + ' ₽';
        }
    }

    // Format all prices on the page
    const priceElements = document.querySelectorAll('.car-price, .car-detail-price');
    priceElements.forEach(formatPrice);
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);


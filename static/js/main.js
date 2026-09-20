/**
 * APEX NUTRITION - Interactive Dark Theme Engine & Cart Management
 */

// CSRF Token Helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Toast Notification System
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `flex items-center gap-3 px-5 py-4 rounded-2xl glass-panel border ${
        type === 'success' ? 'border-emerald-500/40 text-emerald-300' : 'border-red-500/40 text-red-300'
    } shadow-2xl backdrop-blur-xl transform translate-y-4 opacity-0 transition-all duration-300 ease-out z-50`;
    
    const icon = type === 'success' ? 
        '<svg class="w-5 h-5 text-emerald-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>' :
        '<svg class="w-5 h-5 text-red-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';

    toast.innerHTML = `
        ${icon}
        <span class="text-sm font-medium text-white">${message}</span>
    `;

    container.appendChild(toast);

    // Trigger animation
    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-4', 'opacity-0');
    });

    setTimeout(() => {
        toast.classList.add('translate-y-4', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// Add Product to Cart via AJAX
async function addToCart(productId, quantity = 1) {
    try {
        const response = await fetch('/api/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity
            })
        });

        const data = await response.json();
        if (data.success) {
            updateCartBadges(data.cart_count);
            showToast(data.message, 'success');
            // Animate cart icon in navbar
            const cartIcons = document.querySelectorAll('.cart-badge');
            cartIcons.forEach(badge => {
                badge.classList.add('scale-125', 'bg-purple-500');
                setTimeout(() => badge.classList.remove('scale-125', 'bg-purple-500'), 300);
            });
        } else {
            showToast(data.error || 'Ошибка при добавлении в корзину', 'error');
        }
    } catch (err) {
        console.error('Error adding to cart:', err);
        showToast('Не удалось связаться с сервером', 'error');
    }
}

// Update Cart Badges in Navbar
function updateCartBadges(count) {
    const badges = document.querySelectorAll('.cart-count-text');
    badges.forEach(el => {
        el.textContent = count;
        if (count > 0) {
            el.closest('.cart-badge-wrapper')?.classList.remove('hidden');
        }
    });
}

// Update Cart on Checkout Page
async function updateCartQuantity(productId, newQuantity) {
    try {
        const response = await fetch('/api/cart/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: newQuantity
            })
        });

        const data = await response.json();
        if (data.success) {
            updateCartBadges(data.cart_count);
            
            // If item deleted, remove row
            if (newQuantity <= 0) {
                const itemRow = document.getElementById(`cart-item-${productId}`);
                if (itemRow) {
                    itemRow.style.opacity = '0';
                    itemRow.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        itemRow.remove();
                        if (data.cart_count === 0) {
                            location.reload();
                        }
                    }, 300);
                }
            } else {
                // Update quantity display
                const qtyInput = document.getElementById(`qty-val-${productId}`);
                if (qtyInput) qtyInput.textContent = newQuantity;
            }

            // Update subtotal and grand total
            const subtotalEl = document.getElementById('cart-subtotal-val');
            const grandTotalEl = document.getElementById('cart-grandtotal-val');
            const shippingEl = document.getElementById('cart-shipping-val');

            if (subtotalEl) subtotalEl.textContent = `${parseFloat(data.subtotal).toLocaleString('ru-RU')} ₽`;
            if (grandTotalEl) grandTotalEl.textContent = `${parseFloat(data.grand_total).toLocaleString('ru-RU')} ₽`;
            if (shippingEl) shippingEl.textContent = parseFloat(data.shipping_cost) === 0 ? 'Бесплатно' : `${data.shipping_cost} ₽`;
            
            showToast('Корзина обновлена', 'success');
        }
    } catch (err) {
        console.error(err);
        showToast('Ошибка при обновлении корзины', 'error');
    }
}

// Open Quick View Modal
async function openQuickView(productId) {
    const modal = document.getElementById('quick-view-modal');
    if (!modal) return;

    try {
        const response = await fetch(`/api/product/${productId}/`);
        const p = await response.json();

        // Populate Modal Fields
        document.getElementById('modal-img').src = p.image_url;
        document.getElementById('modal-title').textContent = p.title;
        document.getElementById('modal-category').textContent = p.category;
        document.getElementById('modal-tagline').textContent = p.tagline;
        document.getElementById('modal-desc').textContent = p.full_description;
        document.getElementById('modal-price').textContent = `${parseFloat(p.price).toLocaleString('ru-RU')} ₽`;
        
        const oldPriceEl = document.getElementById('modal-old-price');
        if (p.old_price) {
            oldPriceEl.textContent = `${parseFloat(p.old_price).toLocaleString('ru-RU')} ₽`;
            oldPriceEl.classList.remove('hidden');
        } else {
            oldPriceEl.classList.add('hidden');
        }

        document.getElementById('modal-servings').textContent = p.servings || '—';
        document.getElementById('modal-weight').textContent = p.weight_volume || '—';
        document.getElementById('modal-flavor').textContent = p.flavor || '—';
        document.getElementById('modal-rating').textContent = `${p.rating} ★ (${p.reviews_count} отзывов)`;

        // Populate Specs Grid
        const specsContainer = document.getElementById('modal-specs');
        specsContainer.innerHTML = '';
        if (p.specs && typeof p.specs === 'object') {
            for (const [key, val] of Object.entries(p.specs)) {
                const specItem = document.createElement('div');
                specItem.className = 'p-3 rounded-xl bg-zinc-950/70 border border-white/5 flex flex-col justify-between';
                specItem.innerHTML = `
                    <span class="text-xs text-zinc-400 font-medium">${key}</span>
                    <span class="text-sm font-semibold text-white mt-1">${val}</span>
                `;
                specsContainer.appendChild(specItem);
            }
        }

        // Set Add to Cart button in modal
        const modalAddBtn = document.getElementById('modal-add-to-cart-btn');
        modalAddBtn.onclick = () => {
            addToCart(p.id, 1);
            closeQuickView();
        };

        // Open Modal Animation
        modal.classList.remove('hidden');
        setTimeout(() => {
            modal.classList.remove('opacity-0');
            modal.querySelector('.modal-content')?.classList.remove('scale-95');
        }, 10);

        document.body.classList.add('overflow-hidden');
    } catch (err) {
        console.error('Error opening quick view:', err);
    }
}

function closeQuickView() {
    const modal = document.getElementById('quick-view-modal');
    if (!modal) return;
    
    modal.classList.add('opacity-0');
    modal.querySelector('.modal-content')?.classList.add('scale-95');
    setTimeout(() => {
        modal.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
    }, 300);
}

// Goal Quiz Selector (Homepage)
function selectGoal(goalSlug) {
    const buttons = document.querySelectorAll('.goal-btn');
    buttons.forEach(btn => {
        btn.classList.remove('bg-purple-600/30', 'border-purple-500/60', 'text-white');
        btn.classList.add('bg-zinc-900/60', 'border-white/10', 'text-zinc-400');
    });

    const activeBtn = document.getElementById(`goal-btn-${goalSlug}`);
    if (activeBtn) {
        activeBtn.classList.add('bg-purple-600/30', 'border-purple-500/60', 'text-white');
        activeBtn.classList.remove('bg-zinc-900/60', 'border-white/10', 'text-zinc-400');
    }

    const cards = document.querySelectorAll('.goal-product-card');
    cards.forEach(card => {
        const goals = card.dataset.goals || '';
        if (goals.includes(goalSlug) || goalSlug === 'all') {
            card.classList.remove('hidden');
            card.classList.add('flex');
        } else {
            card.classList.add('hidden');
            card.classList.remove('flex');
        }
    });
}

// Mobile Menu Toggle
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    if (!menu) return;
    menu.classList.toggle('hidden');
}

// Initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    // Re-initialize lucide icons if available
    if (window.lucide) {
        window.lucide.createIcons();
    }
});

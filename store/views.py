import json
import uuid
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q
from .models import Category, Product, Order, OrderItem, Review

def get_cart_data(request):
    """
    Helper to extract cart objects and calculate totals from session.
    Cart session structure: { str(product_id): quantity }
    """
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal('0.00')
    total_quantity = 0

    if cart:
        product_ids = [int(pid) for pid in cart.keys() if pid.isdigit()]
        products = Product.objects.filter(id__in=product_ids)
        product_dict = {p.id: p for p in products}

        for pid_str, quantity in cart.items():
            if not pid_str.isdigit():
                continue
            pid = int(pid_str)
            product = product_dict.get(pid)
            if product:
                item_total = product.price * quantity
                subtotal += item_total
                total_quantity += quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'item_total': item_total
                })

    # Free shipping over 5000 ₽ or flat 450 ₽
    shipping_cost = Decimal('0.00') if (subtotal >= 5000 or subtotal == 0) else Decimal('450.00')
    grand_total = subtotal + shipping_cost

    return {
        'items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
        'total_quantity': total_quantity
    }


def home_view(request):
    """
    Страница 1: Главная (Landing Page)
    Флагманы, преимущества, интерактивный квиз подбора, отзывы, хиты.
    """
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True, in_stock=True)
    if not featured_products.exists():
        featured_products = Product.objects.filter(in_stock=True)[:4]
    
    hero_product = Product.objects.filter(slug='gold-standard-100-whey').first() or featured_products.first()
    bestsellers = Product.objects.filter(is_bestseller=True, in_stock=True)[:4]
    if not bestsellers.exists():
        bestsellers = Product.objects.filter(in_stock=True)[:4]

    reviews = Review.objects.filter(is_approved=True)[:6]

    context = {
        'page_title': 'APEX NUTRITION | Премиальное спортивное питание нового поколения',
        'categories': categories,
        'featured_products': featured_products,
        'hero_product': hero_product,
        'bestsellers': bestsellers,
        'reviews': reviews,
    }
    return render(request, 'store/index.html', context)


def catalog_view(request):
    """
    Страница 2: Каталог продукции (Shop with Filters & Search)
    Фильтрация по категориям, поиску, сортировке, быстрый просмотр.
    """
    categories = Category.objects.all()
    products = Product.objects.filter(in_stock=True)

    # Filtering by Category
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug and category_slug != 'all':
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Search query
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(tagline__icontains=query) |
            Q(flavor__icontains=query)
        )

    # Sorting
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating', '-reviews_count')
    elif sort == 'new':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-is_featured', '-is_bestseller', '-created_at')

    context = {
        'page_title': 'Каталог продукции | APEX NUTRITION',
        'categories': categories,
        'selected_category': selected_category,
        'products': products,
        'current_sort': sort,
        'query': query,
    }
    return render(request, 'store/catalog.html', context)


def checkout_view(request):
    """
    Страница 3: Корзина и Оформление заказа (Cart & Checkout)
    Интерактивный расчет, ввод контактов, создание заказа в БД.
    """
    cart_data = get_cart_data(request)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        city = request.POST.get('city', 'Москва').strip()
        address = request.POST.get('address', '').strip()
        payment_method = request.POST.get('payment_method', 'online')
        comment = request.POST.get('comment', '').strip()

        # If cart in session is empty, check if items were passed from direct purchase
        direct_product_id = request.POST.get('direct_product_id')
        
        if direct_product_id:
            try:
                prod = Product.objects.get(id=int(direct_product_id))
                qty = int(request.POST.get('direct_quantity', 1))
                cart_data = {
                    'items': [{'product': prod, 'quantity': qty, 'item_total': prod.price * qty}],
                    'grand_total': prod.price * qty,
                    'discount_amount': Decimal('0.00'),
                }
            except Product.DoesNotExist:
                pass

        if not cart_data['items']:
            return render(request, 'store/checkout.html', {
                'page_title': 'Оформление заказа | APEX NUTRITION',
                'cart': cart_data,
                'error': 'Ваша корзина пуста. Выберите товары в каталоге перед оформлением.'
            })

        if not full_name or not phone or not address:
            return render(request, 'store/checkout.html', {
                'page_title': 'Оформление заказа | APEX NUTRITION',
                'cart': cart_data,
                'error': 'Пожалуйста, заполните обязательные поля: ФИО, телефон и адрес доставки.'
            })

        # Generate unique order number
        order_num = f"APX-{uuid.uuid4().hex[:8].upper()}"
        
        order = Order.objects.create(
            order_number=order_num,
            full_name=full_name,
            phone=phone,
            email=email,
            city=city,
            address=address,
            payment_method=payment_method,
            comment=comment,
            total_price=cart_data['grand_total'],
            discount_amount=Decimal('0.00'),
            status='new'
        )

        for item in cart_data['items']:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        # Clear session cart
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_success', order_number=order.order_number)

    context = {
        'page_title': 'Корзина и Оформление заказа | APEX NUTRITION',
        'cart': cart_data,
    }
    return render(request, 'store/checkout.html', context)


def order_success_view(request, order_number):
    """
    Страница успешного оформления заказа с деталями.
    """
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'page_title': f'Заказ #{order.order_number} оформлен | APEX NUTRITION',
        'order': order,
    }
    return render(request, 'store/order_success.html', context)


# AJAX API Endpoints for dynamic Dark UI interaction
@require_POST
def cart_add_api(request):
    """
    AJAX: Добавить товар в корзину
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
        product_id = str(data.get('product_id'))
        quantity = int(data.get('quantity', 1))

        if not product_id:
            return JsonResponse({'success': False, 'error': 'Не указан ID товара'}, status=400)

        product = get_object_or_404(Product, id=int(product_id))

        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        request.session['cart'] = cart
        request.session.modified = True

        cart_data = get_cart_data(request)

        return JsonResponse({
            'success': True,
            'message': f'«{product.title}» добавлен в корзину!',
            'cart_count': cart_data['total_quantity'],
            'subtotal': str(cart_data['subtotal']),
            'grand_total': str(cart_data['grand_total']),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
def cart_update_api(request):
    """
    AJAX: Обновить количество или удалить товар
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
        product_id = str(data.get('product_id'))
        quantity = int(data.get('quantity', 0))

        cart = request.session.get('cart', {})

        if quantity <= 0:
            if product_id in cart:
                del cart[product_id]
        else:
            cart[product_id] = quantity

        request.session['cart'] = cart
        request.session.modified = True

        cart_data = get_cart_data(request)

        return JsonResponse({
            'success': True,
            'cart_count': cart_data['total_quantity'],
            'subtotal': str(cart_data['subtotal']),
            'shipping_cost': str(cart_data['shipping_cost']),
            'grand_total': str(cart_data['grand_total']),
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_GET
def product_quick_view_api(request, product_id):
    """
    AJAX: Получить полную информацию о товаре для модального окна в темном стиле
    """
    product = get_object_or_404(Product, id=product_id)
    return JsonResponse({
        'id': product.id,
        'title': product.title,
        'category': product.category.name,
        'tagline': product.tagline,
        'short_description': product.short_description,
        'full_description': product.full_description,
        'price': str(product.price),
        'old_price': str(product.old_price) if product.old_price else None,
        'image_url': product.image.url if product.image else '',
        'servings': product.servings,
        'weight_volume': product.weight_volume,
        'flavor': product.flavor,
        'rating': product.rating,
        'reviews_count': product.reviews_count,
        'badge': product.badge,
        'specs': product.specs_json,
    })

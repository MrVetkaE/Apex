import json
from django.test import TestCase, Client
from django.urls import reverse
from store.models import Category, Product, Order, OrderItem, Review

class StoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Протеин",
            slug="protein",
            description="Тестовая категория"
        )
        self.product = Product.objects.create(
            category=self.category,
            title="Gold Standard Whey Test",
            slug="gold-standard-whey-test",
            short_description="Тестовое краткое описание",
            full_description="Тестовое полное описание",
            price=4990.00,
            image="products/on_gold_whey.jpg",
            is_featured=True,
            is_bestseller=True,
            in_stock=True
        )

    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "APEX")
        self.assertContains(response, "Gold Standard Whey Test")

    def test_catalog_page(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Каталог спортивного питания")
        self.assertContains(response, "Gold Standard Whey Test")

    def test_catalog_filter(self):
        response = self.client.get(reverse('catalog') + '?category=protein')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gold Standard Whey Test")

    def test_checkout_page_get(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корзина и оформление")

    def test_ajax_cart_add_and_update(self):
        # 1. Add to cart
        payload = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post(
            reverse('api_cart_add'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 2)

        # 2. Update cart
        update_payload = {'product_id': self.product.id, 'quantity': 3}
        response = self.client.post(
            reverse('api_cart_update'),
            data=json.dumps(update_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 3)

    def test_ajax_product_quick_view(self):
        response = self.client.get(reverse('api_product_quick_view', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], "Gold Standard Whey Test")
        self.assertEqual(data['category'], "Протеин")

    def test_order_submission(self):
        # Add item to session cart first
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()

        order_data = {
            'full_name': 'Тестовый Покупатель',
            'phone': '+7 999 111-22-33',
            'email': 'buyer@test.ru',
            'city': 'Москва',
            'address': 'Красная площадь, д. 1',
            'payment_method': 'online',
            'comment': 'Тестовый заказ'
        }
        response = self.client.post(reverse('checkout'), data=order_data)
        self.assertEqual(response.status_code, 302)

        # Verify order in DB
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.full_name, 'Тестовый Покупатель')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)
        self.assertEqual(order.items.first().quantity, 2)

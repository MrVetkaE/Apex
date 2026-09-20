from django.db import models
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL-идентификатор (slug)")
    description = models.TextField(blank=True, verbose_name="Описание")
    icon = models.CharField(max_length=50, default="dumbbell", verbose_name="Иконка (Lucide)")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Категория")
    title = models.CharField(max_length=200, verbose_name="Название товара")
    slug = models.SlugField(unique=True, verbose_name="URL-идентификатор (slug)")
    tagline = models.CharField(max_length=255, blank=True, verbose_name="Короткий слоган")
    short_description = models.TextField(verbose_name="Краткое описание")
    full_description = models.TextField(verbose_name="Полное описание / О продукте")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (₽)")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Старая цена (₽)")
    image = models.ImageField(upload_to="products/", verbose_name="Изображение товара")
    servings = models.CharField(max_length=100, blank=True, verbose_name="Количество порций")
    weight_volume = models.CharField(max_length=100, blank=True, verbose_name="Вес / Объем")
    flavor = models.CharField(max_length=100, blank=True, verbose_name="Вкус")
    rating = models.FloatField(default=5.0, verbose_name="Рейтинг (от 1 до 5)")
    reviews_count = models.PositiveIntegerField(default=24, verbose_name="Количество отзывов")
    badge = models.CharField(max_length=50, blank=True, verbose_name="Бейдж (Хит, Скидка и т.д.)")
    is_featured = models.BooleanField(default=False, verbose_name="Флагман на главной")
    is_bestseller = models.BooleanField(default=False, verbose_name="Хит продаж")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    specs_json = models.JSONField(default=dict, blank=True, verbose_name="Характеристики / БЖУ (JSON)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-is_featured', '-is_bestseller', '-created_at']

    def __str__(self):
        return self.title

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return int(round(discount))
        return 0


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый заказ'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен / В доставке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    )

    PAYMENT_CHOICES = (
        ('online', 'Банковской картой онлайн (СБП / МИР)'),
        ('courier', 'Оплата при получении курьеру'),
        ('crypto', 'USDT / Криптовалюта'),
    )

    order_number = models.CharField(max_length=32, unique=True, verbose_name="Номер заказа")
    full_name = models.CharField(max_length=150, verbose_name="ФИО покупателя")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Электронная почта")
    city = models.CharField(max_length=100, default="Москва", verbose_name="Город")
    address = models.TextField(verbose_name="Адрес доставки")
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='online', verbose_name="Способ оплаты")
    comment = models.TextField(blank=True, verbose_name="Комментарий к заказу")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма заказа (₽)")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Скидка (₽)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус заказа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ #{self.order_number} ({self.full_name}) - {self.total_price} ₽"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items", verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за шт.")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    @property
    def total_cost(self):
        return self.price * self.quantity


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews", verbose_name="Товар")
    author = models.CharField(max_length=100, verbose_name="Имя автора")
    role_or_city = models.CharField(max_length=100, blank=True, default="PRO Атлет", verbose_name="Статус / Город")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Оценка (1-5)")
    text = models.TextField(verbose_name="Текст отзыва")
    avatar_text = models.CharField(max_length=5, default="AP", verbose_name="Инициалы")
    is_approved = models.BooleanField(default=True, verbose_name="Одобрен для показа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author} ({self.rating}★)"

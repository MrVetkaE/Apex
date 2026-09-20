from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem, Review

# Custom Admin Site Branding
admin.site.site_header = "⚡ APEX NUTRITION | Панель управления"
admin.site.site_title = "APEX Admin"
admin.site.index_title = "Управление магазином спортивного питания"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'products_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = "Товаров в категории"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'category', 'price', 'old_price', 'badge', 'is_featured', 'is_bestseller', 'in_stock')
    list_editable = ('price', 'old_price', 'badge', 'is_featured', 'is_bestseller', 'in_stock')
    list_filter = ('category', 'is_featured', 'is_bestseller', 'in_stock')
    search_fields = ('title', 'short_description', 'tagline', 'flavor')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('image_preview_large', 'created_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 8px; border: 1px solid #444;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Фото"

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 250px; border-radius: 12px; border: 1px solid #555;" />', obj.image.url)
        return "Нет изображения"
    image_preview_large.short_description = "Предпросмотр фото"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'total_cost')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'city', 'total_price', 'status_colored', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'full_name', 'phone', 'email', 'address')
    list_editable = ()
    inlines = [OrderItemInline]
    readonly_fields = ('order_number', 'created_at', 'total_price', 'discount_amount')

    def status_colored(self, obj):
        colors = {
            'new': '#3b82f6',        # Blue
            'processing': '#eab308', # Amber
            'shipped': '#a855f7',    # Purple
            'completed': '#22c55e',  # Green
            'cancelled': '#ef4444',  # Red
        }
        color = colors.get(obj.status, '#71717a')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 12px; font-weight: 600; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = "Статус"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'rating', 'role_or_city', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    search_fields = ('author', 'text', 'role_or_city')

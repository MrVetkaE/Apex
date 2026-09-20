from django.urls import path
from . import views

urlpatterns = [
    # 3 Main Pages
    path('', views.home_view, name='home'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/success/<str:order_number>/', views.order_success_view, name='order_success'),

    # AJAX API Endpoints
    path('api/cart/add/', views.cart_add_api, name='api_cart_add'),
    path('api/cart/update/', views.cart_update_api, name='api_cart_update'),
    path('api/product/<int:product_id>/', views.product_quick_view_api, name='api_product_quick_view'),
]

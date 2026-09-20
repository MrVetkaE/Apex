def cart_context(request):
    """
    Context processor providing cart summary from session.
    """
    cart = request.session.get('cart', {})
    total_items = sum(cart.values()) if isinstance(cart, dict) else 0
    return {
        'cart_count': total_items,
    }

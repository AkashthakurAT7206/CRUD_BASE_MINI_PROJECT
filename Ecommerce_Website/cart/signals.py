from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import transaction
from .models import Cart, CartItem


@receiver(user_logged_in)
def merge_session_cart_into_user_cart(sender, user, request, **kwargs):
    """
    When a user logs in, merge any existing session-based cart into the user's cart.
    After merging, delete the session cart to avoid duplicates.
    """
    # Prefer the pre-login anonymous session key (stored before session rotation),
    # fall back to the current session_key if not present.
    session_key = request.session.get("anon_cart_session_key") or getattr(request.session, "session_key", None)
    if not session_key:
        return

    try:
        session_cart = Cart.objects.prefetch_related("items").get(session_key=session_key, user__isnull=True)
    except Cart.DoesNotExist:
        return

    user_cart, _ = Cart.objects.get_or_create(user=user)

    with transaction.atomic():
        for session_item in session_cart.items.select_related("product"):
            user_item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=session_item.product,
                size=session_item.size,
                defaults={"quantity": session_item.quantity},
            )
            if not created:
                user_item.quantity += session_item.quantity
                user_item.save(update_fields=["quantity"])

        # Remove the session cart after merge
        session_cart.delete()
        # Clean up the flag in session
        if "anon_cart_session_key" in request.session:
            try:
                del request.session["anon_cart_session_key"]
            except Exception:
                pass

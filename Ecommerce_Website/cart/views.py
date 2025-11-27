from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product

# Helper function above here
def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        request.session.save()  # ✅ force save so session_key is persistent
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart



class CartView(View):
    def get(self, request):
        cart = get_cart(request)
        items = cart.items.select_related('product')
        total = cart.get_total_price()
        return render(request, "cart/cart.html", {"cart": cart, "items": items, "total": total})


class AddToCartView(View):
    def post(self, request, product_id):
        cart = get_cart(request)
        product = get_object_or_404(Product, id=product_id)
        available_sizes = product.get_size_options()
        selected_size = (request.POST.get("size") or "").strip()

        if available_sizes:
            if not selected_size:
                messages.error(request, "Please select a size before adding this product to your cart.")
                return redirect("products:product_detail", pk=product.pk)
            if selected_size not in available_sizes:
                messages.error(request, "Invalid size selected for this product.")
                return redirect("products:product_detail", pk=product.pk)
        else:
            selected_size = ""

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=selected_size
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        size_message = f" (Size {selected_size})" if selected_size else ""
        messages.success(request, f"{product.name}{size_message} added to your cart.")
        return redirect("cart:cart_view")


class UpdateCartItemView(View):
    def post(self, request, item_id):
        cart = get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        quantity = int(request.POST.get("quantity", 1))

        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()

        return redirect("cart:cart_view")


class RemoveCartItemView(View):
    def post(self, request, item_id):
        cart = get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        messages.info(request, "Item removed from cart.")
        return redirect("cart:cart_view")


class CheckoutView(View):
    def get(self, request):
        cart = get_cart(request)
        items = cart.items.select_related('product')
        total = cart.get_total_price()
        return render(request, "cart/checkout.html", {"cart": cart, "items": items, "total": total})




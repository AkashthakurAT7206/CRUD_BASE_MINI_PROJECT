from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Wishlist

@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'items': items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user, product=product
    )

    if created:
        messages.success(request, "Added to wishlist ❤")
    else:
        messages.info(request, "This product is already in your wishlist.")

    return redirect('products:product_detail', product_id)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, "Removed from wishlist.")
    return redirect('wishlist:wishlist')

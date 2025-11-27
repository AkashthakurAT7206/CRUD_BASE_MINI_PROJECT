from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from .forms import ReviewForm
from .models import Review

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Prevent duplicate reviews
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.info(request, "You have already reviewed this product.")
        return redirect('products:product_detail', pk=product.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Thank you for reviewing this product!")
            return render(request, 'reviews/thank_you.html', {'product': product})
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_review.html', {'form': form, 'product': product})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by('-created_at')[:5]  # show only 5 latest reviews
    form = ReviewForm()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })


def product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all().order_by('-created_at')

    return render(request, 'reviews/review_list.html', {
        'product': product,
        'reviews': reviews
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from django.urls import reverse
from decimal import Decimal
from .models import Order, OrderItem, Payment
from .forms import OrderForm
from products.models import Product
from cart.views import get_cart
from Accounts.models import UserAddress


import razorpay
from razorpay.errors import SignatureVerificationError
from django.conf import settings



class OrderCreateView(LoginRequiredMixin, View):
    """Create a new order (checkout)"""
    template_name = 'orders/order_create.html'
    
    def get(self, request):
        user_address = getattr(request.user, 'address', None)
        initial_data = user_address.to_order_initial() if user_address else {}
        form = OrderForm(initial=initial_data)
        # Build cart summary for the checkout page
        cart = get_cart(request)
        cart_items_qs = cart.items.select_related('product') if cart else None

        items_data = []
        subtotal = Decimal('0.00')

        if cart_items_qs and cart_items_qs.exists():
            for ci in cart_items_qs:
                product = ci.product
                quantity = ci.quantity
                price = product.discount_price if product.discount_price else product.price
                item_subtotal = price * quantity
                subtotal += item_subtotal
                items_data.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price,
                    'subtotal': item_subtotal,
                    'size': ci.size
                })
        else:
            session_cart = request.session.get('cart', {})
            for product_id, item_data in session_cart.items():
                try:
                    product = Product.objects.get(id=int(product_id))
                    quantity = item_data.get('quantity', 1)
                    price = product.discount_price if product.discount_price else product.price
                    item_subtotal = price * quantity
                    subtotal += item_subtotal
                    items_data.append({
                        'product': product,
                        'quantity': quantity,
                        'price': price,
                        'subtotal': item_subtotal,
                        'size': item_data.get('size', '')
                    })
                except Product.DoesNotExist:
                    continue

        tax = subtotal * Decimal('0.10') if subtotal > 0 else Decimal('0.00')
        shipping_cost = Decimal('50.00') if subtotal > 0 else Decimal('0.00')
        total = subtotal + tax + shipping_cost

        change_address_url = f"{reverse('address_update')}?next={request.path}"

        return render(request, self.template_name, {
            'form': form,
            'page_title': 'Checkout',
            'cart_items': items_data,
            'subtotal': subtotal,
            'tax': tax,
            'shipping_cost': shipping_cost,
            'total': total,
            'saved_address': user_address,
            'address_change_url': change_address_url,
        })
    
    @transaction.atomic
    def post(self, request):
        form = OrderForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form, 'page_title': 'Checkout'})
        # Prefer using the site's Cart model (if cart exists for user or session)
        cart = get_cart(request)
        cart_items_qs = cart.items.select_related('product') if cart else None

        items_data = []
        subtotal = Decimal('0.00')

        if cart_items_qs and cart_items_qs.exists():
            for ci in cart_items_qs:
                product = ci.product
                quantity = ci.quantity
                price = product.discount_price if product.discount_price else product.price
                item_subtotal = price * quantity
                subtotal += item_subtotal
                items_data.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price,
                    'subtotal': item_subtotal,
                    'size': ci.size
                })
        else:
            # Fallback to session-based cart (legacy or anonymous carts stored in session)
            session_cart = request.session.get('cart', {})
            if not session_cart:
                messages.error(request, 'Your cart is empty.')
                return redirect('orders:create')

            for product_id, item_data in session_cart.items():
                try:
                    product = Product.objects.get(id=int(product_id))
                    quantity = item_data.get('quantity', 1)
                    price = product.discount_price if product.discount_price else product.price
                    item_subtotal = price * quantity
                    subtotal += item_subtotal
                    items_data.append({
                        'product': product,
                        'quantity': quantity,
                        'price': price,
                        'subtotal': item_subtotal,
                        'size': item_data.get('size', '')
                    })
                except Product.DoesNotExist:
                    continue

        if not items_data:
            messages.error(request, 'No valid items in cart.')
            return redirect('orders:create')
        
        tax = subtotal * Decimal('0.10')
        shipping_cost = Decimal('50.00')
        order = form.save(commit=False)
        order.user = request.user
        order.subtotal = subtotal
        order.tax = tax
        order.shipping_cost = shipping_cost
        order.save()

        # Persist address for future checkouts
        UserAddress.objects.update_or_create(
            user=request.user,
            defaults={
                'address_line': form.cleaned_data['shipping_address'],
                'city': form.cleaned_data['shipping_city'],
                'state': form.cleaned_data['shipping_state'],
                'zip_code': form.cleaned_data['shipping_zip_code'],
                'country': form.cleaned_data['shipping_country'],
                'phone_number': form.cleaned_data['shipping_phone'],
            }
        )
        
        for item in items_data:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
                subtotal=item['subtotal'],
                size=item.get('size', '')
            )
        # Clear the cart: remove cart items if using the Cart model, otherwise clear session cart
        try:
            if cart and hasattr(cart, 'items'):
                cart.items.all().delete()
            else:
                request.session['cart'] = {}
        except Exception:
            # In case clearing cart fails, at least clear session representation
            request.session['cart'] = {}
        messages.success(request, f'Order {order.order_number} created!')
        return redirect('orders:detail', order_id=order.id)


class OrderListView(LoginRequiredMixin, View):
    """List all orders (admin) or user's orders"""
    template_name = 'orders/order_list.html'
    
    def get(self, request):
        if request.user.is_staff:
            orders = Order.objects.all().order_by('-created_at')
        else:
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
        
        paginator = Paginator(orders, 10)
        page_obj = paginator.get_page(request.GET.get('page'))
        
        return render(request, self.template_name, {'orders': page_obj, 'page_title': 'Orders'})


class OrderDetailView(LoginRequiredMixin, View):
    """Display order details"""
    template_name = 'orders/order_detail.html'
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        
        if not request.user.is_staff and order.user != request.user:
            messages.error(request, 'Permission denied.')
            return redirect('orders:list')
        
        return render(request, self.template_name, {
            'order': order,
            'order_items': order.items.all(),
            'page_title': f'Order {order.order_number}'
        })


class OrderSuccessView(LoginRequiredMixin, View):
    """Order success page"""
    template_name = 'orders/order_success.html'
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(request, self.template_name, {'order': order, 'page_title': 'Order Success'})


@login_required
def cancel_order(request, order_id):
    """Cancel an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status in ['cancelled', 'delivered', 'refunded']:
        messages.error(request, f'Cannot cancel order with status: {order.get_status_display()}')
        return redirect('orders:detail', order_id=order.id)
    
    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order {order.order_number} cancelled.')
        return redirect('orders:detail', order_id=order.id)
    
    return redirect('orders:detail', order_id=order.id)



# def start_payment(request):
#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#     amount = 50000  # 500 = ₹500

#     order_data = {
#         "amount": amount,
#         "currency": "INR",
#         "payment_capture": "1",
#     }

#     order = client.order.create(data=order_data)

#     return render(request, "orders/payment.html", {
#         "order_id": order["id"],
#         "amount": amount,
#         "key_id": settings.RAZORPAY_KEY_ID
#     })

@login_required
def start_payment(request, order_id):
    """Initiate payment for an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if order already has a completed payment
    if order.payment_status:
        messages.info(request, 'This order has already been paid.')
        return redirect('orders:detail', order_id=order.id)
    
    # Check if payment method requires gateway
    if order.payment_method == 'cod':
        # For COD, create a payment record with completed status
        payment = Payment.objects.create(
            order=order,
            amount=order.total,
            payment_method=order.payment_method,
            payment_gateway='cod',
            status='completed'
        )
        payment.mark_as_completed()
        messages.success(request, 'Order placed successfully. Payment will be collected on delivery.')
        return redirect('orders:detail', order_id=order.id)
    
    # For online payments, use Razorpay
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Convert rupees to paise
        amount_paise = int(order.total * 100)
        
        # Create Razorpay order
        razorpay_order_data = {
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": "1",
            "notes": {
                "order_id": order.id,
                "order_number": order.order_number,
            }
        }
        
        razorpay_order = client.order.create(data=razorpay_order_data)
        
        # Create payment record
        payment = Payment.objects.create(
            order=order,
            amount=order.total,
            payment_method=order.payment_method,
            payment_gateway='razorpay',
            razorpay_order_id=razorpay_order['id'],
            status='pending',
            gateway_response=razorpay_order
        )
        
        return render(request, "orders/payment.html", {
            "order": order,
            "payment": payment,
            "razorpay_order_id": razorpay_order['id'],
            "amount": amount_paise,
            "amount_rupees": order.total,
            "key_id": settings.RAZORPAY_KEY_ID,
        })
    except Exception as e:
        messages.error(request, f'Payment initialization failed: {str(e)}')
        return redirect('orders:detail', order_id=order.id)


@login_required
def payment_success(request):
    """Handle successful payment callback from Razorpay"""

    # Razorpay sends GET request, not POST
    if request.method in ['GET', 'POST']:

        razorpay_payment_id = request.GET.get('razorpay_payment_id') or request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.GET.get('razorpay_order_id') or request.POST.get('razorpay_order_id')
        razorpay_signature = request.GET.get('razorpay_signature') or request.POST.get('razorpay_signature')

        try:
            payment = Payment.objects.get(
                razorpay_order_id=razorpay_order_id
            )

            # Verify signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            try:
                client.utility.verify_payment_signature(params_dict)

                # Update payment
                payment.razorpay_payment_id = razorpay_payment_id
                payment.razorpay_signature = razorpay_signature
                payment.status = 'processing'
                payment.save()

                # Fetch payment status
                razorpay_payment = client.payment.fetch(razorpay_payment_id)

                if razorpay_payment['status'] == 'captured':
                    payment.mark_as_completed()
                    payment.order.status = "PAID"          # 🔥 update order status
                    payment.order.save()

                    messages.success(request, f'Payment successful! Order {payment.order.order_number} confirmed.')
                    return redirect('orders:detail', order_id=payment.order.id)
                else:
                    payment.status = 'failed'
                    payment.failure_reason = f"Payment status: {razorpay_payment.get('status', 'unknown')}"
                    payment.save()

                    payment.order.status = "FAILED"
                    payment.order.save()

                    messages.error(request, 'Payment verification failed.')
                    return redirect('orders:detail', order_id=payment.order.id)

            except SignatureVerificationError:
                payment.mark_as_failed("Signature verification failed")
                payment.order.status = "FAILED"
                payment.order.save()

                messages.error(request, 'Payment verification failed.')
                return redirect('orders:detail', order_id=payment.order.id)

        except Payment.DoesNotExist:
            messages.error(request, 'Payment record not found.')
            return redirect('orders:list')

    return redirect('orders:list')



@login_required
def payment_failure(request):
    """Handle failed payment callback"""
    if request.method == 'POST':
        razorpay_order_id = request.POST.get('razorpay_order_id')
        error_description = request.POST.get('error_description', 'Payment failed')
        
        try:
            payment = Payment.objects.get(
                razorpay_order_id=razorpay_order_id,
                status__in=['pending', 'processing']
            )
            payment.mark_as_failed(error_description)
            messages.error(request, f'Payment failed: {error_description}')
            return redirect('orders:detail', order_id=payment.order.id)
        except Payment.DoesNotExist:
            messages.error(request, 'Payment record not found.')
            return redirect('orders:list')
    
    return redirect('orders:list')


class PaymentHistoryView(LoginRequiredMixin, View):
    """View payment history for a user"""
    template_name = 'orders/payment_history.html'
    
    def get(self, request):
        if request.user.is_staff:
            payments = Payment.objects.all().order_by('-created_at')
        else:
            payments = Payment.objects.filter(order__user=request.user).order_by('-created_at')
        
        paginator = Paginator(payments, 10)
        page_obj = paginator.get_page(request.GET.get('page'))
        
        return render(request, self.template_name, {
            'payments': page_obj,
            'page_title': 'Payment History'
        })


class PaymentDetailView(LoginRequiredMixin, View):
    """View payment details"""
    template_name = 'orders/payment_detail.html'
    
    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id)
        
        # Check permissions
        if not request.user.is_staff and payment.order.user != request.user:
            messages.error(request, 'Permission denied.')
            return redirect('orders:payment_history')
        
        return render(request, self.template_name, {
            'payment': payment,
            'order': payment.order,
            'page_title': f'Payment {payment.payment_id}'
        })
    


@login_required
def invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    # Add total price (quantity × product price) for each item
    total_amount = 0
    for item in order_items:
        item.total_price = item.quantity * item.product.price
        total_amount += item.total_price

    return render(request, "orders/invoice.html", {
        "order": order,
        "order_items": order_items,
        "total_amount": total_amount,
    })

def save(self, *args, **kwargs):
    self.shipping_cost = Decimal('0.00')  # FORCE shipping = 0 always
    
    if not self.order_number:
        self.order_number = generate_order_number()

    # Always re-calculate total
    self.total = self.subtotal + self.tax + self.shipping_cost
    
    super().save(*args, **kwargs)

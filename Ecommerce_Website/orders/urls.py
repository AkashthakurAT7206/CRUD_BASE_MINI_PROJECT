from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('', views.OrderListView.as_view(), name='list'),
    path('<int:order_id>/', views.OrderDetailView.as_view(), name='detail'),
    path('<int:order_id>/success/', views.OrderSuccessView.as_view(), name='success'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    
    # Payment URLs
    path('payment/<int:order_id>/', views.start_payment, name='start_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
    path('payments/', views.PaymentHistoryView.as_view(), name='payment_history'),
    path('payment/<int:payment_id>/', views.PaymentDetailView.as_view(), name='payment_detail'),

    path('invoice/<int:order_id>/', views.invoice, name='invoice'),
]

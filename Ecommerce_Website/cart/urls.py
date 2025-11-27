from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart_view'),
    path('add/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='update_cart_item'),
    path('remove/<int:item_id>/', views.RemoveCartItemView.as_view(), name='remove_cart_item'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]


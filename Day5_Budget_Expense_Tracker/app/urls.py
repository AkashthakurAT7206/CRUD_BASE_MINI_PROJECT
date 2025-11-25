from django.urls import path
from .views import (
    # Transaction URLs
    TransactionListView,
    TransactionDetailView,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionDeleteView,
    # Category URLs
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    # Budget URLs
    BudgetListView,
    BudgetCreateView,
    BudgetUpdateView,
    BudgetDeleteView,
)

urlpatterns = [
    # Transaction URLs
    path('', TransactionListView.as_view(), name='transaction_list'),
    path('transaction/detail/<int:pk>/', TransactionDetailView.as_view(), name='transaction_detail'),
    path('transaction/create/', TransactionCreateView.as_view(), name='transaction_create'),
    path('transaction/update/<int:pk>/', TransactionUpdateView.as_view(), name='transaction_update'),
    path('transaction/delete/<int:pk>/', TransactionDeleteView.as_view(), name='transaction_delete'),
    
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    
    # Budget URLs
    path('budgets/', BudgetListView.as_view(), name='budget_list'),
    path('budget/create/', BudgetCreateView.as_view(), name='budget_create'),
    path('budget/update/<int:pk>/', BudgetUpdateView.as_view(), name='budget_update'),
    path('budget/delete/<int:pk>/', BudgetDeleteView.as_view(), name='budget_delete'),
]

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Sum, Q
from .models import Transaction, Category, Budget
from .forms import TransactionForm, CategoryForm, BudgetForm


# Transaction Views
class TransactionListView(ListView):
    model = Transaction
    template_name = 'app/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate totals
        transactions = Transaction.objects.all()
        context['total_income'] = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_expense'] = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        context['balance'] = context['total_income'] - context['total_expense']
        return context


class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'app/transaction_detail.html'
    context_object_name = 'transaction'


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'app/transaction_form.html'
    success_url = reverse_lazy('transaction_list')


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'app/transaction_form.html'
    success_url = reverse_lazy('transaction_list')


class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'app/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')


# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'app/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'app/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'app/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'app/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


# Budget Views
class BudgetListView(ListView):
    model = Budget
    template_name = 'app/budget_list.html'
    context_object_name = 'budgets'


class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'app/budget_form.html'
    success_url = reverse_lazy('budget_list')


class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'app/budget_form.html'
    success_url = reverse_lazy('budget_list')


class BudgetDeleteView(DeleteView):
    model = Budget
    template_name = 'app/budget_confirm_delete.html'
    success_url = reverse_lazy('budget_list')

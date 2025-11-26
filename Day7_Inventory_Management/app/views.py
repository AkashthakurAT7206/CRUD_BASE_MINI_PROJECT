from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Sum, F
from .models import Product, Category, Supplier, StockMovement
from .forms import ProductForm, CategoryForm, SupplierForm, StockMovementForm


# Dashboard View
class DashboardView(ListView):
    model = Product
    template_name = 'app/dashboard.html'
    context_object_name = 'products'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        
        # Calculate dashboard statistics
        context['total_products'] = products.count()
        context['low_stock_products'] = products.filter(quantity_in_stock__lte=F('reorder_level')).count()
        context['total_inventory_value'] = sum([p.total_value for p in products])
        context['total_categories'] = Category.objects.count()
        context['total_suppliers'] = Supplier.objects.count()
        context['recent_movements'] = StockMovement.objects.all()[:5]
        
        return context


# Product Views
class ProductListView(ListView):
    model = Product
    template_name = 'app/product_list.html'
    context_object_name = 'products'
    paginate_by = 20


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movements'] = self.object.movements.all()[:10]
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'app/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'app/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'app/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')


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


# Supplier Views
class SupplierListView(ListView):
    model = Supplier
    template_name = 'app/supplier_list.html'
    context_object_name = 'suppliers'


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'app/supplier_form.html'
    success_url = reverse_lazy('supplier_list')


class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'app/supplier_form.html'
    success_url = reverse_lazy('supplier_list')


class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'app/supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier_list')


# Stock Movement Views
class StockMovementListView(ListView):
    model = StockMovement
    template_name = 'app/stock_movement_list.html'
    context_object_name = 'movements'
    paginate_by = 50


class StockMovementCreateView(CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'app/stock_movement_form.html'
    success_url = reverse_lazy('stock_movement_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Update product stock based on movement type
        movement = self.object
        product = movement.product
        
        if movement.movement_type == 'in':
            product.quantity_in_stock += movement.quantity
        elif movement.movement_type == 'out':
            product.quantity_in_stock -= movement.quantity
        elif movement.movement_type == 'adjustment':
            product.quantity_in_stock = movement.quantity
        
        product.save()
        return response


class StockMovementDeleteView(DeleteView):
    model = StockMovement
    template_name = 'app/stock_movement_confirm_delete.html'
    success_url = reverse_lazy('stock_movement_list')

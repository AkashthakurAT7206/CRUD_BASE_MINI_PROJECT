from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Category
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# List all products
# class HomeView(View):
#     template_name = 'products/home.html'

#     def get(self, request):
#         # Fetch only 4 categories (for homepage display)
#         categories = Category.objects.filter(is_active=True)[:4]
#         return render(request, self.template_name, {'categories': categories})

def home(request):
    return render(request,'base.html')

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 30  # Optional pagination

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(name__icontains=query, available=True)
        return Product.objects.filter(available=True)


# Product details
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


# List all categories
class CategoryListView(ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'


# Products filtered by category
class CategoryProductsView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        try:
            category = Category.objects.get(slug=category_slug, is_active=True)
            return Product.objects.filter(category=category, available=True)
        except Category.DoesNotExist:
            return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        try:
            context['category'] = Category.objects.get(slug=category_slug, is_active=True)
        except Category.DoesNotExist:
            context['category'] = None
        return context


# Create new product
class ProductCreateView(CreateView):
    model = Product
    fields = ['category', 'name', 'sku', 'description', 'price', 'discount_price',
             'stock', 'available', 'brand', 'image', 'tags', 'available_sizes', 'rating']
    template_name = 'products/add_product.html'
    success_url = reverse_lazy('products:product_list')


# Update product
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['category', 'name', 'sku', 'description', 'price', 'discount_price',
             'stock', 'available', 'brand', 'image', 'tags', 'available_sizes', 'rating']
    template_name = 'products/update_product.html'
    success_url = reverse_lazy('products:product_list')


# Delete product
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    success_url = reverse_lazy('products:product_list')



from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'available', 'brand', 'created_at')
    list_filter = ('available', 'category', 'brand')
    search_fields = ('name', 'sku', 'tags', 'brand')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('available',)









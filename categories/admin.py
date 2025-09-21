from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_count', 'is_active', 'created_at', 'image_preview', 'actions_column')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    ordering = ('title',)
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_editable = ('is_active',)
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'is_active'),
            'classes': ('wide',)
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('products')
        )
    
    def product_count(self, obj):
        count = obj.product_count
        if count > 0:
            url = reverse('admin:products_product_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} products</a>', url, count)
        return '0 products'
    product_count.short_description = 'Products'
    product_count.admin_order_field = 'product_count'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; border: 1px solid #ddd; border-radius: 4px; object-fit: cover; background: #f8f9fa;" alt="{}" />',
                obj.image.url, obj.title
            )
        return format_html('<span style="color: #999;">No image</span>')
    image_preview.short_description = 'Image Preview'
    
    def actions_column(self, obj):
        return format_html(
            '<a class="button" href="{}">View Products</a>',
            reverse('admin:products_product_changelist') + f'?category__id__exact={obj.id}'
        )
    actions_column.short_description = 'Actions'
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update Elasticsearch index if products exist
        if obj.products.exists():
            from products.documents import ProductDocument
            for product in obj.products.all():
                ProductDocument().update(product)

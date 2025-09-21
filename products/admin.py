from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock_quantity', 'stock_status', 'is_active', 'created_at', 'image_preview', 'actions_column')
    list_filter = ('category', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'category__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_editable = ('price', 'stock_quantity', 'is_active')
    list_per_page = 25
    raw_id_fields = ('category',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category'),
            'classes': ('wide',)
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity', 'is_active'),
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
    
    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            return format_html('<span style="color: red;">Out of Stock</span>')
        elif obj.stock_quantity < 10:
            return format_html('<span style="color: orange;">Low Stock ({})</span>', obj.stock_quantity)
        else:
            return format_html('<span style="color: green;">In Stock ({})</span>', obj.stock_quantity)
    stock_status.short_description = 'Stock Status'
    stock_status.admin_order_field = 'stock_quantity'
    
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
            '<a class="button" href="{}">View Details</a>',
            reverse('admin:products_product_change', args=[obj.pk])
        )
    actions_column.short_description = 'Actions'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update Elasticsearch index
        from products.documents import ProductDocument
        ProductDocument().update(obj)
        
        # Show stock warning
        if obj.stock_quantity < 10:
            messages.warning(request, f'Warning: {obj.title} has low stock ({obj.stock_quantity} items)')
    
    actions = ['mark_as_active', 'mark_as_inactive', 'update_elasticsearch_index']
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products marked as active.')
    mark_as_active.short_description = 'Mark selected products as active'
    
    def mark_as_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products marked as inactive.')
    mark_as_inactive.short_description = 'Mark selected products as inactive'
    
    def update_elasticsearch_index(self, request, queryset):
        from products.documents import ProductDocument
        for product in queryset:
            ProductDocument().update(product)
        self.message_user(request, f'Updated Elasticsearch index for {queryset.count()} products.')
    update_elasticsearch_index.short_description = 'Update Elasticsearch index'


admin.site.register(Product, ProductAdmin)

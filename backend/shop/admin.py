from django.contrib import admin
from django.utils.html import format_html 
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Sum, Avg
from .models import Category, Product, ProductReview, Cart, CartItem, Order, OrderItem, Wishlist

class CartItemInline(admin.TabularInline):
    """Inline for cart items"""
    model = CartItem
    extra = 0
    fields = ['product', 'quantity', 'total']
    readonly_fields = ['total']
    can_delete = True
    
    def total(self, obj):
        return obj.total
    total.short_description = 'Total'


class OrderItemInline(admin.TabularInline):
    """Inline for order items"""
    model = OrderItem
    extra = 0
    fields = ['product', 'quantity', 'price', 'total']
    readonly_fields = ['total']
    can_delete = False
    
    def total(self, obj):
        return obj.total
    total.short_description = 'Total'


class ProductInline(admin.TabularInline):
    """Inline for wishlist products"""
    model = Wishlist.products.through
    extra = 0
    verbose_name = 'Product'
    verbose_name_plural = 'Products'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin"""
    
    list_display = [
        'id', 'name', 'slug', 'product_count', 'is_active', 
        'created_at', 'category_icon'
    ]
    
    prepopulated_fields = {'slug': ('name',)}
    
    list_filter = ['is_active', 'parent', 'created_at']
    
    search_fields = ['name', 'description']
    
    list_editable = ['is_active']
    
    readonly_fields = ['created_at', 'updated_at', 'product_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'parent', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Statistics', {
            'fields': ('product_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def product_count(self, obj):
        """Count products in category"""
        count = obj.products.count()
        url = reverse('admin:shop_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{}</a>', url, count)
    product_count.short_description = 'Products'
    
    def category_icon(self, obj):
        """Show category icon"""
        if obj.image:
            return format_html('<img src="{}" style="width: 30px; height: 30px; object-fit: cover;" />', obj.image.url)
        return 'No Image'
    category_icon.short_description = 'Icon'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product Admin"""
    
    list_display = [
        'id', 'product_image', 'name', 'category', 'price', 'compare_at_price',
        'quantity', 'stock_status', 'is_featured', 'is_active', 'sales_count'
    ]
    
    prepopulated_fields = {'slug': ('name',)}
    
    list_filter = ['category', 'is_active', 'is_featured', 'is_new', 'brand', 'created_at']
    
    search_fields = ['name', 'sku', 'description', 'brand']
    
    list_editable = ['price', 'quantity', 'is_active', 'is_featured']
    
    readonly_fields = ['views_count', 'sales_count', 'created_at', 'updated_at', 'product_preview']
    
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'sku', 'description', 'short_description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'compare_at_price', 'cost_price', 'quantity', 'low_stock_threshold', 'track_inventory')
        }),
        ('Product Details', {
            'fields': ('brand', 'material', 'color', 'size', 'weight', 'dimensions')
        }),
        ('Images', {
            'fields': ('image', 'image2', 'image3', 'image4', 'product_preview')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_new', 'is_active')
        }),
        ('Statistics', {
            'fields': ('views_count', 'sales_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_featured', 'remove_featured', 'make_active', 'make_inactive']
    
    def product_image(self, obj):
        """Show product thumbnail"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return 'No Image'
    product_image.short_description = 'Image'
    
    def product_preview(self, obj):
        """Show all product images"""
        html = '<div style="display: flex; gap: 10px;">'
        for img in obj.all_images:
            html += f'<img src="{img}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 4px;" />'
        html += '</div>'
        return format_html(html)
    product_preview.short_description = 'Image Preview'
    
    def stock_status(self, obj):
        """Display stock status with colors"""
        if obj.quantity <= 0:
            return format_html('<span style="color: red; font-weight: bold;">Out of Stock</span>')
        elif obj.quantity <= obj.low_stock_threshold:
            return format_html('<span style="color: orange; font-weight: bold;">Low Stock ({})</span>', obj.quantity)
        else:
            return format_html('<span style="color: green;">In Stock ({})</span>', obj.quantity)
    stock_status.short_description = 'Stock Status'
    
    def make_featured(self, request, queryset):
        """Make selected products featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} products marked as featured.')
    make_featured.short_description = "Mark as featured"
    
    def remove_featured(self, request, queryset):
        """Remove featured from selected products"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} products removed from featured.')
    remove_featured.short_description = "Remove from featured"
    
    def make_active(self, request, queryset):
        """Make selected products active"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products activated.')
    make_active.short_description = "Activate products"
    
    def make_inactive(self, request, queryset):
        """Make selected products inactive"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products deactivated.')
    make_inactive.short_description = "Deactivate products"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """Product Review Admin"""
    
    list_display = [
        'id', 'product', 'user', 'rating_stars', 'is_approved', 
        'is_verified_purchase', 'created_at'
    ]
    
    list_filter = ['rating', 'is_approved', 'is_verified_purchase', 'created_at']
    
    search_fields = ['product__name', 'user__email', 'comment']
    
    list_editable = ['is_approved']
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'user', 'rating', 'title', 'comment')
        }),
        ('Status', {
            'fields': ('is_approved', 'is_verified_purchase')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def rating_stars(self, obj):
        """Display rating as stars"""
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        color = '#f39c12' if obj.rating >= 4 else '#e67e22' if obj.rating >= 3 else '#e74c3c'
        return format_html('<span style="color: {};">{}</span>', color, stars)
    rating_stars.short_description = 'Rating'
    
    def approve_reviews(self, request, queryset):
        """Approve selected reviews"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} reviews approved.')
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        """Disapprove selected reviews"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} reviews disapproved.')
    disapprove_reviews.short_description = "Disapprove selected reviews"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart Admin"""
    
    list_display = ['id', 'user', 'session_id', 'total_items', 'subtotal', 'created_at']
    
    list_filter = ['created_at']
    
    search_fields = ['user__email', 'session_id']
    
    readonly_fields = ['created_at', 'updated_at']
    
    inlines = [CartItemInline]
    
    def total_items(self, obj):
        """Total items in cart"""
        return obj.total_items
    total_items.short_description = 'Items'
    
    def subtotal(self, obj):
        """Cart subtotal"""
        return f"K{obj.subtotal:.2f}"
    subtotal.short_description = 'Subtotal'


# backend/shop/admin.py - Fixed OrderAdmin

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order Admin"""
    
    list_display = [
        'order_number', 'user', 'full_name', 'total', 'status_badge',
        'payment_status_badge', 'payment_method_icon', 'created_at'
    ]
    
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    
    search_fields = ['order_number', 'user__email', 'first_name', 'last_name']
    
    readonly_fields = ['order_number', 'subtotal', 'tax', 'total', 'created_at', 'updated_at']
    
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status', 'payment_method')
        }),
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Shipping Information', {
            'fields': ('shipping_method', 'tracking_number')
        }),
        ('Financial', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'discount', 'total')
        }),
        ('Additional', {
            'fields': ('notes', 'ip_address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    # ============ CUSTOM METHODS ============
    
    def status_badge(self, obj):
        """Display status with colors"""
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'confirmed': 'teal',
            'shipped': 'purple',
            'delivered': 'green',
            'cancelled': 'red',
            'refunded': 'gray',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 0.8rem;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'  # Allows sorting by status
    
    def payment_status_badge(self, obj):
        """Display payment status with colors"""
        colors = {
            'pending': 'orange',
            'paid': 'green',
            'failed': 'red',
            'refunded': 'gray',
        }
        color = colors.get(obj.payment_status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 0.8rem;">{}</span>',
            color, obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment'
    payment_status_badge.admin_order_field = 'payment_status'
    
    def payment_method_icon(self, obj):
        """Display payment method with icon"""
        icons = {
            'card': '💳',
            'mobile_money': '📱',
            'cash': '💵',
            'bank_transfer': '🏦',
        }
        icon = icons.get(obj.payment_method, '💰')
        method = obj.get_payment_method_display()
        return format_html('{} {}', icon, method)
    payment_method_icon.short_description = 'Method'
    payment_method_icon.admin_order_field = 'payment_method'
    
    def full_name(self, obj):
        """Return customer full name"""
        return obj.full_name
    full_name.short_description = 'Customer'
    full_name.admin_order_field = 'first_name'
    
    # ============ ACTIONS ============
    
    def mark_as_processing(self, request, queryset):
        """Mark orders as processing"""
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} orders marked as processing.')
    mark_as_processing.short_description = "Mark as processing"
    
    def mark_as_shipped(self, request, queryset):
        """Mark orders as shipped"""
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} orders marked as shipped.')
    mark_as_shipped.short_description = "Mark as shipped"
    
    def mark_as_delivered(self, request, queryset):
        """Mark orders as delivered"""
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} orders marked as delivered.')
    mark_as_delivered.short_description = "Mark as delivered"
    
    def mark_as_cancelled(self, request, queryset):
        """Mark orders as cancelled"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} orders marked as cancelled.')
    mark_as_cancelled.short_description = "Mark as cancelled"


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Wishlist Admin"""
    
    list_display = ['id', 'user', 'name', 'product_count', 'is_public', 'created_at']
    
    list_filter = ['is_public', 'created_at']
    
    search_fields = ['user__email', 'name']
    
    readonly_fields = ['created_at', 'updated_at']
    
    filter_horizontal = ['products']
    
    def product_count(self, obj):
        """Count products in wishlist"""
        return obj.products.count()
    product_count.short_description = 'Products'

from django.contrib import admin
# backend/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Address, UserActivity, Notification

class AddressInline(admin.TabularInline):
    """Inline for user addresses"""
    model = Address
    extra = 0
    fields = ['address_type', 'full_name', 'city', 'country', 'is_default', 'phone']
    readonly_fields = ['created_at', 'updated_at']

class UserActivityInline(admin.TabularInline):
    """Inline for user activities"""
    model = UserActivity
    extra = 0
    fields = ['activity_type', 'description', 'ip_address', 'created_at']
    readonly_fields = ['created_at']
    can_delete = False

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    
    # Display fields in user list
    list_display = [
        'id', 'email', 'username', 'full_name', 'phone_number', 
        'is_active', 'is_staff', 'date_joined', 'profile_picture_preview'
    ]
    
    # Filters
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'newsletter_subscription', 'date_joined']
    
    # Search fields
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone_number']
    
    # Default ordering
    ordering = ['-date_joined']
    
    # Fields to display in detail view
    fieldsets = (
        ('Login Information', {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_picture')
        }),
        ('Preferences', {
            'fields': ('newsletter_subscription',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    
    # Fields for adding new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff'),
        }),
    )
    
    # Inlines
    inlines = [AddressInline, UserActivityInline]
    
    # Read-only fields
    readonly_fields = ['date_joined', 'last_login', 'profile_picture_preview']
    
    def full_name(self, obj):
        """Display full name"""
        return obj.full_name
    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'first_name'
    
    def profile_picture_preview(self, obj):
        """Show profile picture preview"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.profile_picture.url
            )
        return 'No Image'
    profile_picture_preview.short_description = 'Profile Picture'
    
    # Actions
    actions = ['activate_users', 'deactivate_users', 'send_newsletter']
    
    def activate_users(self, request, queryset):
        """Activate selected users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users were successfully activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users were successfully deactivated.')
    deactivate_users.short_description = "Deactivate selected users"
    
    def send_newsletter(self, request, queryset):
        """Send newsletter to selected users"""
        self.message_user(request, 'Newsletter feature coming soon!')
    send_newsletter.short_description = "Send newsletter to selected users"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Address Admin"""
    
    list_display = [
        'id', 'user', 'full_name', 'address_type', 'city', 'country', 
        'is_default', 'phone', 'created_at'
    ]
    
    list_filter = ['address_type', 'is_default', 'country', 'city']
    
    search_fields = ['user__email', 'first_name', 'last_name', 'city', 'phone']
    
    list_editable = ['is_default']
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'address_type')
        }),
        ('Name', {
            'fields': ('first_name', 'last_name', 'company')
        }),
        ('Address Details', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Contact', {
            'fields': ('phone',)
        }),
        ('Settings', {
            'fields': ('is_default', 'delivery_instructions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """User Activity Admin"""
    
    list_display = ['id', 'user', 'activity_type', 'description', 'ip_address', 'created_at']
    
    list_filter = ['activity_type', 'created_at']
    
    search_fields = ['user__email', 'user__username', 'description', 'ip_address']
    
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        """Prevent manual addition of activities"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent editing of activities"""
        return False


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification Admin"""
    
    list_display = ['id', 'user', 'notification_type', 'title', 'is_read', 'created_at']
    
    list_filter = ['notification_type', 'is_read', 'is_archived', 'created_at']
    
    search_fields = ['user__email', 'title', 'message']
    
    list_editable = ['is_read']
    
    readonly_fields = ['created_at']
    
    actions = ['mark_as_read', 'mark_as_unread', 'archive_selected']
    
    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifications marked as read.')
    mark_as_read.short_description = "Mark selected as read"
    
    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notifications marked as unread.')
    mark_as_unread.short_description = "Mark selected as unread"
    
    def archive_selected(self, request, queryset):
        """Archive selected notifications"""
        updated = queryset.update(is_archived=True)
        self.message_user(request, f'{updated} notifications archived.')
    archive_selected.short_description = "Archive selected"

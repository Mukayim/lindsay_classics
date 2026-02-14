from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# ============================================
# Custom User Model (if you want to extend User)
# ============================================

class User(AbstractUser):
    """Extended User model"""
    
    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_set",  # Custom related_name
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",  # Custom related_name
        related_query_name="custom_user",
    )
    
    # Contact Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+260123456789'"
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Profile
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Preferences
    newsletter_subscription = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

# ============================================
# Address Model
# ============================================

class Address(models.Model):
    """User shipping/billing addresses"""
    
    ADDRESS_TYPES = [
        ('shipping', 'Shipping'),
        ('billing', 'Billing'),
        ('both', 'Both'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='both')
    
    # Address fields
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Zambia')
    
    # Contact
    phone = models.CharField(max_length=20)
    
    # Additional
    is_default = models.BooleanField(default=False)
    delivery_instructions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"
    
    def save(self, *args, **kwargs):
        # If this address is set as default, unset other default addresses
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def full_address(self):
        address = self.address_line1
        if self.address_line2:
            address += f", {self.address_line2}"
        address += f", {self.city}"
        if self.state:
            address += f", {self.state}"
        address += f", {self.postal_code}, {self.country}"
        return address

# ============================================
# User Activity Log
# ============================================

class UserActivity(models.Model):
    """Track user activity for analytics"""
    
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view_product', 'View Product'),
        ('add_to_cart', 'Add to Cart'),
        ('remove_from_cart', 'Remove from Cart'),
        ('place_order', 'Place Order'),
        ('view_order', 'View Order'),
        ('add_review', 'Add Review'),
        ('update_profile', 'Update Profile'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)  # Store additional data
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "User activities"
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.created_at}"

# ============================================
# User Notification
# ============================================

class Notification(models.Model):
    """User notifications"""
    
    NOTIFICATION_TYPES = [
        ('order', 'Order Update'),
        ('promotion', 'Promotion'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True)  # URL to redirect to
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

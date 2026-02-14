from django.urls import path
from . import views

urlpatterns = [
    # User registration and authentication
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # User profile
    path('profile/', views.get_user_profile, name='profile'),
    path('profile/update/', views.update_user_profile, name='profile_update'),
    
    # Password management
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
    # User management (admin only)
    path('list/', views.list_users, name='list_users'),
    path('detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path('update/<int:user_id>/', views.admin_update_user, name='admin_update_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    # Address management
    path('addresses/', views.user_addresses, name='user_addresses'),
    path('addresses/add/', views.add_address, name='add_address'),
    path('addresses/<int:address_id>/', views.update_address, name='update_address'),
    path('addresses/<int:address_id>/delete/', views.delete_address, name='delete_address'),
]
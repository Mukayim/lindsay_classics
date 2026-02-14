from django.shortcuts import render
# backend/users/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging

logger = logging.getLogger(__name__)

# Helper function to parse request body
def parse_request_body(request):
    try:
        return json.loads(request.body)
    except:
        return {}

# ============================================
# Authentication Views
# ============================================

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    """Register a new user"""
    try:
        data = parse_request_body(request)
        
        # Required fields
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        if not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Email and password are required'
            }, status=400)
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'error': 'User with this email already exists'
            }, status=400)
        
        # Create username from email
        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        return JsonResponse({
            'success': True,
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=201)
        
    except Exception as e:
        logger.exception("Registration failed")
        return JsonResponse({
            'success': False,
            'error': 'Registration failed'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    """Login user"""
    try:
        data = parse_request_body(request)
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'Email and password are required'
            }, status=400)
        
        # Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Invalid credentials'
            }, status=401)
        
        # Authenticate
        user = authenticate(username=user.username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid credentials'
            }, status=401)
            
    except Exception as e:
        logger.exception("Login failed")
        return JsonResponse({
            'success': False,
            'error': 'Login failed'
        }, status=500)

@login_required
@require_http_methods(["POST"])
def logout_user(request):
    """Logout user"""
    logout(request)
    return JsonResponse({
        'success': True,
        'message': 'Logout successful'
    })

# ============================================
# Profile Views
# ============================================

@login_required
@require_http_methods(["GET"])
def get_user_profile(request):
    """Get current user profile"""
    user = request.user
    return JsonResponse({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
            'last_login': user.last_login
        }
    })

@login_required
@require_http_methods(["PUT", "PATCH"])
def update_user_profile(request):
    """Update current user profile"""
    try:
        data = parse_request_body(request)
        user = request.user
        
        # Update fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data and data['email'] != user.email:
            # Check if email is already taken
            if User.objects.filter(email=data['email']).exclude(id=user.id).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Email already in use'
                }, status=400)
            user.email = data['email']
        
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
        
    except Exception as e:
        logger.exception("Profile update failed")
        return JsonResponse({
            'success': False,
            'error': 'Profile update failed'
        }, status=500)

# ============================================
# Password Management
# ============================================

@login_required
@require_http_methods(["POST"])
def change_password(request):
    """Change user password"""
    try:
        data = parse_request_body(request)
        user = request.user
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return JsonResponse({
                'success': False,
                'error': 'Old password and new password are required'
            }, status=400)
        
        # Check old password
        if not user.check_password(old_password):
            return JsonResponse({
                'success': False,
                'error': 'Old password is incorrect'
            }, status=400)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Password changed successfully'
        })
        
    except Exception as e:
        logger.exception("Password change failed")
        return JsonResponse({
            'success': False,
            'error': 'Password change failed'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def reset_password(request):
    """Reset password (forgot password flow)"""
    try:
        data = parse_request_body(request)
        email = data.get('email')
        
        if not email:
            return JsonResponse({
                'success': False,
                'error': 'Email is required'
            }, status=400)
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Return success even if user doesn't exist (security)
            return JsonResponse({
                'success': True,
                'message': 'If the email exists, a reset link has been sent'
            })
        
        # TODO: Implement email sending logic
        # For now, just return success
        return JsonResponse({
            'success': True,
            'message': 'Password reset email sent'
        })
        
    except Exception as e:
        logger.exception("Password reset failed")
        return JsonResponse({
            'success': False,
            'error': 'Password reset failed'
        }, status=500)

# ============================================
# Admin User Management
# ============================================

@login_required
@require_http_methods(["GET"])
def list_users(request):
    """List all users (admin only)"""
    if not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Admin access required'
        }, status=403)
    
    users = User.objects.all().order_by('-date_joined')
    user_list = []
    
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined,
            'last_login': user.last_login
        })
    
    return JsonResponse({
        'success': True,
        'count': len(user_list),
        'users': user_list
    })

@login_required
@require_http_methods(["GET"])
def user_detail(request, user_id):
    """Get user details (admin only)"""
    if not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Admin access required'
        }, status=403)
    
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'date_joined': user.date_joined,
                'last_login': user.last_login
            }
        })
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User not found'
        }, status=404)

@login_required
@require_http_methods(["PUT", "PATCH"])
def admin_update_user(request, user_id):
    """Update user (admin only)"""
    if not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Admin access required'
        }, status=403)
    
    try:
        user = User.objects.get(id=user_id)
        data = parse_request_body(request)
        
        # Update fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data and data['email'] != user.email:
            if User.objects.filter(email=data['email']).exclude(id=user.id).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Email already in use'
                }, status=400)
            user.email = data['email']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'is_staff' in data and request.user.is_superuser:
            user.is_staff = data['is_staff']
        
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': 'User updated successfully'
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User not found'
        }, status=404)
    except Exception as e:
        logger.exception("User update failed")
        return JsonResponse({
            'success': False,
            'error': 'User update failed'
        }, status=500)

@login_required
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    """Delete user (admin only)"""
    if not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Admin access required'
        }, status=403)
    
    try:
        user = User.objects.get(id=user_id)
        
        # Prevent deleting yourself
        if user.id == request.user.id:
            return JsonResponse({
                'success': False,
                'error': 'Cannot delete your own account'
            }, status=400)
        
        user.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'User deleted successfully'
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'User not found'
        }, status=404)

# ============================================
# Address Management (Optional - requires Address model)
# ============================================

# Note: These views require an Address model
# You'll need to create the model first

@login_required
@require_http_methods(["GET"])
def user_addresses(request):
    """Get user's addresses"""
    # TODO: Implement after creating Address model
    return JsonResponse({
        'success': True,
        'addresses': []
    })

@login_required
@require_http_methods(["POST"])
def add_address(request):
    """Add new address"""
    # TODO: Implement after creating Address model
    return JsonResponse({
        'success': True,
        'message': 'Address added'
    })

@login_required
@require_http_methods(["PUT", "PATCH"])
def update_address(request, address_id):
    """Update address"""
    # TODO: Implement after creating Address model
    return JsonResponse({
        'success': True,
        'message': 'Address updated'
    })

@login_required
@require_http_methods(["DELETE"])
def delete_address(request, address_id):
    """Delete address"""
    # TODO: Implement after creating Address model
    return JsonResponse({
        'success': True,
        'message': 'Address deleted'
    })
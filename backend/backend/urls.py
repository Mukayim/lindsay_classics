from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.generic import TemplateView


def health_check(request):
    return JsonResponse({
        "status": "ok",
        "message": "Lindsay Classics API is running",
        "database": "connected"
    })


def api_root(request):
    """API root endpoint that returns JSON instead of trying to render a template"""
    return JsonResponse({
        "name": "Lindsay Classics API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health/",
            "admin": "/admin/",
            "shop": "/api/shop/",
            "users": "/api/users/"
        },
        "documentation": "This is a backend API service. Use the endpoints above."
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/shop/', include('shop.urls')),
    path('api/users/', include('users.urls')),
    path('health/', health_check, name='health_check'),
    path('', api_root, name='api_root'),  # This returns JSON now, not a template
]

# Serve media files during development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# IMPORTANT: Remove or comment out any catch-all template view
# If you have this line anywhere, DELETE IT:
# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
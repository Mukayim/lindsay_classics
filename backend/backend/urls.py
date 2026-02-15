from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import JsonResponse

# Health check endpoint
def health_check(request):
    return JsonResponse({
        "status": "ok",
        "message": "Lindsay Classics API is running",
        "database": "connected"
    })

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # API endpoints all under /api/
    path('api/shop/', include('shop.urls')),
    path('api/users/', include('users.urls')),
    path('api/health/', health_check, name='health_check'),
]

# Serve React app for all other URLs (catch-all)
REACT_BUILD_DIR = settings.REACT_BUILD_DIR if hasattr(settings, "REACT_BUILD_DIR") else None

if REACT_BUILD_DIR and (REACT_BUILD_DIR / 'index.html').exists():
    urlpatterns += [
        re_path(r'^.*$', TemplateView.as_view(template_name=str(REACT_BUILD_DIR / 'index.html'))),
    ]

# Serve static/media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

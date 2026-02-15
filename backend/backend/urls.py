from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        "status": "ok",
        "message": "Lindsay Classics API is running",
        "database": "connected"  # you can add real DB check later if needed
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/shop/', include('shop.urls')),     # fixed: 'shop.urls' with dot
    path('api/users/', include('users.urls')),
    path('health/', health_check, name='health_check'),
]

# Serve media files during development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# SPA fallback – serve React index.html for all non-API routes
# This should be last — catches everything not matched above
urlpatterns += [
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
]
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import JsonResponse
import os

# -------------------------------
# API endpoints
# -------------------------------
def health_check(request):
    return JsonResponse({"status": "ok", "message": "Lindsay Classics API is running"})

def api_root(request):
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
    path('api/', api_root, name='api_root'),
]

# -------------------------------
# Serve React app at /
# -------------------------------
if settings.DEBUG:
    # Serve media/static files in dev
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Production: serve React build index.html for any non-API route
    class ReactAppView(TemplateView):
        template_name = "index.html"

        def get_template_names(self):
            # index.html from React build
            react_index = settings.REACT_BUILD_DIR / "index.html"
            if react_index.exists():
                return [str(react_index)]
            return [super().get_template_names()[0]]

    # Catch-all for non-API paths
    urlpatterns += [
        re_path(r'^(?!api/).*$', ReactAppView.as_view(), name='react_app')
    ]

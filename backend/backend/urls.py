from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "message": "Welcome to Lindsay Classics API",
        "endpoints": {
            "admin": "/admin/",
            "shop": "/api/shop/",
            "users": "/api/users/",
        },
        "frontend": "http://localhost:5173"
    })

urlpatterns = [
    path('', api_root, name='api_root'),  # Add this line
    path('admin/', admin.site.urls),
    path('api/shop/', include('shop.urls')),
    path('api/users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
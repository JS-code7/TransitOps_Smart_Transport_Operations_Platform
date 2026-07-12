from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "status": "online",
        "message": "TransitOps Backend API Server is running",
        "api_root": "/api/"
    })

urlpatterns = [
    path('', root_view),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

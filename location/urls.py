from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from properties.views import PropertyViewSet, FavoriteViewSet
from django.conf import settings
from django.conf.urls.static import static

# DRF Router
router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename="property")
router.register(r'favorites', FavoriteViewSet, basename="favorite")


urlpatterns = [
    path('api/', include(router.urls)),   # API REST
    path('admin/', admin.site.urls),      # Django Admin
]

# Servir les fichiers médias et statiques en mode debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

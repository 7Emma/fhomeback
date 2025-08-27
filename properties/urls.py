from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, toggle_favorite, get_user_favorites, check_favorite

# Router pour les ViewSets
router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename="property")

urlpatterns = [
    # Utilise le routeur pour gérer toutes les URL de PropertyViewSet
    path("", include(router.urls)),
    
    # Laisse les URLs manuelles pour les autres vues (favoris, etc.)
    path("favorites/toggle/", toggle_favorite, name="toggle_favorite"),
    path("favorites/", get_user_favorites, name="get_user_favorites"),
    path("favorites/check/<int:property_id>/", check_favorite, name="check_favorite"),
]
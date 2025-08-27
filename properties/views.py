from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Property, Favorite
from .serializers import PropertySerializer, FavoriteSerializer

# ----------------------
# CRUD Propriétés
# ----------------------
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by("-date_added")
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

# ----------------------
# Favoris
# ----------------------
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def toggle_favorite(request):
    property_id = request.data.get("property_id")
    property_instance = get_object_or_404(Property, id=property_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, property=property_instance)

    if not created:
        favorite.delete()
        return Response({"message": "Retiré des favoris"}, status=status.HTTP_200_OK)

    return Response({"message": "Ajouté aux favoris"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_user_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def check_favorite(request, property_id):
    exists = Favorite.objects.filter(user=request.user, property_id=property_id).exists()
    return Response({"is_favorite": exists})

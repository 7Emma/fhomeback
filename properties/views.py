from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Property, Favorite
from .serializers import PropertySerializer, FavoriteSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

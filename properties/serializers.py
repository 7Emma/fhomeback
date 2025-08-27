from rest_framework import serializers
from .models import Property, Favorite, PropertyImage

# Nouveau sérialiseur pour le modèle PropertyImage
# Il est nécessaire pour sérialiser le champ 'image'
class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ('image',) # Vous pouvez ajouter d'autres champs si nécessaire

# Sérialiseur pour le modèle Property
class PropertySerializer(serializers.ModelSerializer):
    # Ajoutez cette ligne pour inclure les images liées à la propriété
    # 'many=True' gère la liste d'images
    # 'read_only=True' empêche la création d'images lors de la création d'une propriété
    images = PropertyImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Property
        # '__all__' inclut tous les champs du modèle Property, et maintenant le champ 'images' que nous venons d'ajouter.
        fields = '__all__'

# Le reste du fichier est inchangé
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
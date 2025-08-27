# properties/serializers.py

from rest_framework import serializers
from .models import Property, PropertyImage, Favorite

class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ["id", "image", "image_url", "is_main"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    video = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = "__all__"

    def get_video(self, obj):
        request = self.context.get("request")
        if obj.video and request is not None:
            return request.build_absolute_uri(obj.video.url)
        return None

class FavoriteSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "property"]
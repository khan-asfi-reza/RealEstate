from django.utils.translation import ugettext as _
from rest_framework import serializers

from .models import Property, Property_Video, Property_Images


# Serializer for Property Model


# Serializer for Property Image Model
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property_Images
        fields = (

            'property',
            'image',
            'image_name',
            'image_type'
        )


# Serializer for Property Video Model
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property_Video
        fields = (
            'property',
            'video',
            'video_name'
        )


# Serializer for Property
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'agent', 'owner', 'name', 'description', 'bathrooms', 'bedrooms', 'kitchen',
                  'living_area', 'rent', 'parking_spot', 'parking_number', 'land_size', 'indoor_size',
                  'location', 'lease_length', 'date_available', 'features', 'property_type', 'walkthrough',
                  'floor_plan']

        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs.get('agent') is None and attrs.get('owner') is None:
            msg = _('Missing agent or owner')
            raise serializers.ValidationError(msg)
        return attrs

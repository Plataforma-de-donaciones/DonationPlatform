from rest_framework import serializers
from .models import ArticlesZones

class ArticlesZonesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlesZones
        fields = '__all__'


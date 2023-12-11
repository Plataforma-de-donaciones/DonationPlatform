from rest_framework import serializers
from .models import ArticlesType

class ArticlesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlesType
        fields = '__all__'


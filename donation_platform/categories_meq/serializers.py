from rest_framework import serializers
from .models import CategoriesMeq

class CategoriesMeqSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesMeq
        fields = '__all__'


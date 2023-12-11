from rest_framework import serializers
from .models import CategoriesMeq

class CategoriesMeqSerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source='cat.cat_name', read_only=True)

    class Meta:
        model = CategoriesMeq
        fields = ['id', 'cat_id', 'eq_id', 'cat_name']


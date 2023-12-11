from rest_framework import serializers
from .models import CategoriesDon

class CategoriesDonSerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source='cat.cat_name', read_only=True)

    class Meta:
        model = CategoriesDon
        fields = ['id', 'cat_id', 'don_id', 'cat_name']


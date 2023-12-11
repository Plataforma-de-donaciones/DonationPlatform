from rest_framework import serializers
from .models import ArticlesStates

class ArticlesStatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlesStates
        fields = '__all__'


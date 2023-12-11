from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

    image = serializers.ImageField(max_length=None, use_url=True, required=False)

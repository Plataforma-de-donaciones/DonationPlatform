from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    image = serializers.ImageField(max_length=None, use_url=True, required=False)


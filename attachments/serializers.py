from rest_framework import serializers
from .models import Attachments

class AttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachments
        fields = '__all__'


from rest_framework import serializers
from .models import MedicalEquipment

class MedicalEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalEquipment
        fields = '__all__'

    image = serializers.ImageField(max_length=None, use_url=True, required=False)


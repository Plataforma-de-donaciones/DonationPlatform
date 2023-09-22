from rest_framework import serializers
from .models import MedicalEquipment

class MedicalEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalEquipment
        fields = '__all__'


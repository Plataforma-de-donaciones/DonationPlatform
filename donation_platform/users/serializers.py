from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        #exclude = ('user_password',)
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'GET':
            data.pop('user_password', None)
        return data

class UsersSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['user_password', 'id', 'user_email']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

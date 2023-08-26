from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Users
from .serializers import UsersSerializer
from django.utils import timezone

class UsersListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

class UsersCreateView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
       # Implementación de eliminación lógica
       instance.user_state = 0
       instance.erased_at = timezone.now()  # Marcar la fecha de eliminación
       instance.save()

from django.shortcuts import render
from rest_framework import generics, permissions
#from django.db.models import Q
from .models import ArticlesZones
from .serializers import ArticlesZonesSerializer
from django.utils import timezone
from rest_framework.response import Response

class ArticlesZonesListView(generics.ListCreateAPIView):
    queryset = ArticlesZones.objects.all()
    serializer_class = ArticlesZonesSerializer
    permission_classes = [permissions.IsAuthenticated]

class ArticlesZonesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticlesZones.objects.all()
    serializer_class = ArticlesZonesSerializer
    permission_classes = [permissions.IsAuthenticated]


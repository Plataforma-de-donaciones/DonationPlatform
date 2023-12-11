from django.shortcuts import render
from rest_framework import generics, permissions
#from django.db.models import Q
from .models import ArticlesType
from .serializers import ArticlesTypeSerializer
from django.utils import timezone
from rest_framework.response import Response

class ArticlesTypeListView(generics.ListCreateAPIView):
    queryset = ArticlesType.objects.all()
    serializer_class = ArticlesTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ArticlesTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticlesType.objects.all()
    serializer_class = ArticlesTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


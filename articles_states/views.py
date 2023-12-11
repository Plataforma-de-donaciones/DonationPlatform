from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import ArticlesStates
from .serializers import ArticlesStatesSerializer
from django.utils import timezone
from rest_framework.response import Response

class ArticlesStatesListView(generics.ListCreateAPIView):
    queryset = ArticlesStates.objects.all()
    serializer_class = ArticlesStatesSerializer
    permission_classes = [permissions.IsAuthenticated]

class ArticlesStatesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticlesStates.objects.all()
    serializer_class = ArticlesStatesSerializer
    permission_classes = [permissions.IsAuthenticated]


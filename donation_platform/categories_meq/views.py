from django.shortcuts import render
from rest_framework import generics, permissions
#from django.db.models import Q
from .models import CategoriesMeq
from .serializers import CategoriesMeqSerializer
from django.utils import timezone
from rest_framework.response import Response

class CategoriesMeqListView(generics.ListCreateAPIView):
    queryset = CategoriesMeq.objects.all()
    serializer_class = CategoriesMeqSerializer

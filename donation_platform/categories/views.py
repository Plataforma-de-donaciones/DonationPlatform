from django.shortcuts import render
from rest_framework import generics, permissions
#from django.db.models import Q
from .models import Categories
from .serializers import CategoriesSerializer
from django.utils import timezone
from rest_framework.response import Response

class CategoriesListView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

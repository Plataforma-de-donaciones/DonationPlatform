from django.shortcuts import render
from rest_framework import generics, permissions, status
#from django.db.models import Q
from .models import CategoriesMeq
from .serializers import CategoriesMeqSerializer
from django.utils import timezone
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404


class CategoriesMeqListView(generics.ListCreateAPIView):
    queryset = CategoriesMeq.objects.all()
    serializer_class = CategoriesMeqSerializer

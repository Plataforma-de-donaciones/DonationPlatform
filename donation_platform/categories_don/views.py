from django.shortcuts import render
from rest_framework import generics, permissions, status
#from django.db.models import Q
from .models import CategoriesDon
from .serializers import CategoriesDonSerializer
from django.utils import timezone
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView

class CategoriesDonListView(generics.ListCreateAPIView):
    queryset = CategoriesDon.objects.all()
    serializer_class = CategoriesDonSerializer

class CategoriesDonSearchViewByCatId(ListCreateAPIView):
    serializer_class = CategoriesDonSerializer

    def get_queryset(self):
        cat_id = self.kwargs.get('cat_id')
        queryset = CategoriesDon.objects.filter(Q(cat_id=cat_id))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

from django.shortcuts import render
from rest_framework import generics, permissions, status
#from django.db.models import Q
from .models import CategoriesMeq
from .serializers import CategoriesMeqSerializer
from django.utils import timezone
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView

class CategoriesMeqListView(generics.ListCreateAPIView):
    queryset = CategoriesMeq.objects.all()
    serializer_class = CategoriesMeqSerializer

class CategoriesMeqSearchViewByCatId(ListCreateAPIView):
    serializer_class = CategoriesMeqSerializer

    def get_queryset(self):
        cat_id = self.kwargs.get('cat_id')
        queryset = CategoriesMeq.objects.filter(Q(cat_id=cat_id))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

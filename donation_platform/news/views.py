from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import News
from .serializers import NewsSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
import logging
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

class NewsListView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    #permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save()

class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

class NewsSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            news = News.objects.filter(
                Q(user__user_name__exact=search_param) |
                Q(user__user_email__exact=search_param)
            )

            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class NewsSearchViewbyName(generics.ListAPIView):
    serializer_class = NewsSerializer

    def post(self, request):
        new_name = self.request.data.get('new_name', '')
        logger = logging.getLogger(__name__)
        logger.debug("Valor de username: %s", new_name)

        queryset = News.objects.filter(
            Q(new_name__icontains=new_name)
        )
        logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class NewsSearchViewbySubject(generics.ListAPIView):
    serializer_class = NewsSerializer

    def post(self, request):
        new_subject = self.request.data.get('new_subject', '')
        logger = logging.getLogger(__name__)
        logger.debug("Valor de username: %s", new_subject)

        queryset = News.objects.filter(
            Q(new_subject__icontains=new_subject)
        )
        logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class NewsSearchViewbyId(generics.ListAPIView):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        new_id = self.request.data.get('new_id', '')
        #logger = logging.getLogger(__name__)
        #logger.debug("Valor de username: %s", eq_name)

        queryset = News.objects.filter(
            Q(new_id__exact=new_id)
        )
        #logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


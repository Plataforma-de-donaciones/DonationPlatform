from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
import logging
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
#from rest_framework.parsers import MultiPartParser, FormParser

class MessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    #permission_classes = [permissions.IsAuthenticated]

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            try:
                id = int(search_param)
                message = Message.objects.filter(Q(user__id=id) | Q(user__user_name=search_param) | Q(user__user_email__exact=search_param))
            except ValueError:
                # Si no es un número, busca por type_name
                message = Message.objects.filter( Q(user__user_name=search_param) | Q(user__user_email__exact=search_param))

            serializer = MessageSerializer(message, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class MessageSearchViewbyId(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        mess_id = self.request.data.get('mess_id', '')

        queryset = Message.objects.filter(
            Q(mess_id__exact=mess_id)
        )
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


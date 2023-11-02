from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Chat
from .serializers import ChatSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
import logging
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
#from rest_framework.parsers import MultiPartParser, FormParser

class ChatListView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            try:
                id = int(search_param)
                chat = Chat.objects.filter(Q(user__id=id) | Q(user__user_name=search_param) | Q(user__user_email__exact=search_param))
            except ValueError:
                # Si no es un número, busca por type_name
                chat = Chat.objects.filter( Q(user__user_name=search_param) | Q(user__user_email__exact=search_param))

            serializer = ChatSerializer(Chat, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'Chat': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class ChatSearchViewbyId(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        chat_id = self.request.data.get('chat_id', '')

        queryset = Chat.objects.filter(
            Q(chat_id__exact=chat_id)
        )
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


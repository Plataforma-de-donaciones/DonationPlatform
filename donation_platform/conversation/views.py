from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Conversation
from .serializers import ConversationSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
import logging
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
#from rest_framework.parsers import MultiPartParser, FormParser

class ConversationListView(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

#class ConversationSearchViewbyUser(APIView):
 #   permission_classes = [permissions.IsAuthenticated]

  #  def post(self, request):
   #     search_param = request.data.get('search', '')

    #    if search_param:
     #       try:
      #          id = int(search_param)
       #         conversation = Conversation.objects.filter(Q(user__id=id) | Q(user__user_name=search_param) | Q(user__user_email__exact=search_param))
        #    except ValueError:
         #       # Si no es un número, busca por type_name
          #      conversation = Conversation.objects.filter( Q(user__user_name=search_param) | Q(user__user_email__exact=search_param))

           # serializer = ConversationSerializer(equipments, many=True)
           # return Response(serializer.data, status=status.HTTP_200_OK)

        #return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)
class ConversationSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            try:
                id = int(search_param)
                conversation = Conversation.objects.filter(Q(user_1__id=id) | Q(user_2__id=id))
            except ValueError:
                # Si no es un número, busca por name o email
                conversation = Conversation.objects.filter(Q(user_1__user_name=search_param) | Q(user_2__user_name=search_param) | Q(user_1__user_email__exact=search_param) | Q(user_2__user_email__exact=search_param))

            serializer = ConversationSerializer(conversation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class ConversationSearchViewbyId(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        conv_id = self.request.data.get('conv_id', '')

        queryset = Conversation.objects.filter(
            Q(conv_id__exact=conv_id)
        )
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


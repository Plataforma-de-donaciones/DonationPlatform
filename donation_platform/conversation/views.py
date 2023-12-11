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
from users.models import Users

#from rest_framework.parsers import MultiPartParser, FormParser

class ConversationListView(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        data_with_user_info = []
        for conversation_data in response.data:
            user_1_id = conversation_data.get('user_1')
            user_2_id = conversation_data.get('user_2')

            try:
                user_1 = Users.objects.get(id=user_1_id)
                user_2 = Users.objects.get(id=user_2_id)

                user_1_info = {
                    'user_id': user_1.id,
                    'user_name': user_1.user_name,
                    'user_email': user_1.user_email,
                }

                user_2_info = {
                    'user_id': user_2.id,
                    'user_name': user_2.user_name,
                    'user_email': user_2.user_email,
                }

                conversation_data['user_1_info'] = user_1_info
                conversation_data['user_2_info'] = user_2_info
            except Users.DoesNotExist:
                conversation_data['user_1_info'] = None
                conversation_data['user_2_info'] = None

            data_with_user_info.append(conversation_data)

        response.data = data_with_user_info
        return response

class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            try:
                id = int(search_param)
                conversations = Conversation.objects.filter(Q(user_1__id=id) | Q(user_2__id=id))
            except ValueError:
                conversations = Conversation.objects.filter(Q(user_1__user_name=search_param) | Q(user_2__user_name=search_param) | Q(user_1__user_email__exact=search_param) | Q(user_2__user_email__exact=search_param))

            data_with_user_info = []
            for conversation_data in ConversationSerializer(conversations, many=True).data:
                user_1_id = conversation_data.get('user_1')
                user_2_id = conversation_data.get('user_2')

                try:
                    user_1 = Users.objects.get(id=user_1_id)
                    user_2 = Users.objects.get(id=user_2_id)

                    user_1_info = {
                        'user_id': user_1.id,
                        'user_name': user_1.user_name,
                        'user_email': user_1.user_email,
                    }

                    user_2_info = {
                        'user_id': user_2.id,
                        'user_name': user_2.user_name,
                        'user_email': user_2.user_email,
                    }

                    conversation_data['user_1_info'] = user_1_info
                    conversation_data['user_2_info'] = user_2_info
                except Users.DoesNotExist:
                    conversation_data['user_1_info'] = None
                    conversation_data['user_2_info'] = None

                data_with_user_info.append(conversation_data)

            return Response(data_with_user_info, status=status.HTTP_200_OK)

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


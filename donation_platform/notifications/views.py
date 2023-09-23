from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Notifications
from .serializers import NotificationsSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
import logging
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView

class NotificationsListView(generics.ListCreateAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationsSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            notifications = Notifications.objects.filter(
                Q(user__user_name__exact=search_param) |
                Q(user__user_email__exact=search_param)
            )

            serializer = NotificationsSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)


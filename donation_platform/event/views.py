from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Event
from .serializers import EventSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
import logging
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView

class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    #permission_classes = [permissions.IsAuthenticated]

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    #def perform_destroy(self, instance):
       # Implementación de eliminación lógica
       #instance.administrator_state = 0
       #instance.erased_at = timezone.now()  # Marcar la fecha de eliminación
       #instance.save()

class EventSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            events = Event.objects.filter(
                Q(user__user_name__exact=search_param) |
                Q(user__user_email__exact=search_param)
            )

            serializer = EventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class EventSearchViewbyName(generics.ListAPIView):
    serializer_class = EventSerializer

    def post(self, request):
        event_name = self.request.data.get('event_name', '')
        logger = logging.getLogger(__name__)
        logger.debug("Valor de username: %s", event_name)

        queryset = Event.objects.filter(
            Q(event_name__icontains=event_name)
        )
        logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class EventSearchViewbyType(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            events = Event.objects.filter(
                Q(type__type_name__exact=search_param)
            )

            serializer = EventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)


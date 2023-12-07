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
from rest_framework.parsers import MultiPartParser, FormParser
import subprocess
import json
import logging
import re
from unidecode import unidecode


class EventListView(generics.ListCreateAPIView):
    #queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = Event.objects.filter(end_date__gte=timezone.now()).order_by('start_date')
        return queryset

    def perform_create(self, serializer):
        serializer.save()

        event_name = serializer.instance.event_name
        event_description = serializer.instance.event_description

        normalized_name = normalize_text(event_name)
        normalized_description = normalize_text(event_description)

        command = f'curl -H "Authorization: Bearer CDCAER5NSNNBBJHC3WHQVOHHOZTGLTLI" "https://api.wit.ai/message?v=20231202&q={normalized_name}%20{normalized_description}"'

        output = subprocess.check_output(command, shell=True)

        etiqueta_ofensiva = analizar_respuesta(output)

        if etiqueta_ofensiva == 'ofensivo':
            serializer.instance.end_date = timezone.now()
            serializer.instance.geom_point = 'Oculto'
        serializer.instance.save()

def analizar_respuesta(respuesta):

    try:
        respuesta_decodificada = respuesta.decode('utf-8')

        respuesta_json = json.loads(respuesta_decodificada)

        return 'ofensivo' if any(intent['name'] in ['insulto', 'ilegal'] for intent in respuesta_json.get('intents', [])) else 'no_ofensivo'
    except (json.JSONDecodeError, AttributeError) as e:
        return 'error'

def normalize_text(text):
    text = unidecode(re.sub(r'[^A-Za-záéíóúüÁÉÍÓÚÜñÑ\s]', '', text))
    text = text.replace(" ", "%20")
    return text


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

class EventSearchViewbyTypeUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_type_param = request.data.get('search_type', '')
        search_user_param = request.data.get('search_user', '')

        if search_type_param or search_user_param:
            query = Q()

            if search_type_param:
                query &= (Q(type__type_name__exact=search_type_param) | Q(type__type_id=search_type_param))

            if search_user_param:
                query &= (Q(user__user_name__exact=search_user_param) | Q(user__user_email__exact=search_user_param))

            events = Event.objects.filter(query)

            serializer = EventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese al menos un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class EventSearchViewbyId(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        event_id = self.request.data.get('event_id', '')

        queryset = Event.objects.filter(
            Q(event_id__exact=event_id)
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class EventListOcultView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = Event.objects.filter(end_date__isnull=False, geom_point__isnull=False)
        return queryset


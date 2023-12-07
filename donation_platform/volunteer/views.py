from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Volunteer
from .serializers import VolunteerSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
import logging
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
import subprocess
import json
import logging
import re
from unidecode import unidecode

class VolunteerListView(generics.ListCreateAPIView):
    serializer_class = VolunteerSerializer

    def get_queryset(self):
        queryset = Volunteer.objects.filter(end_date__isnull=True)
        return queryset
    def perform_create(self, serializer):
        serializer.save()

        vol_name = serializer.instance.vol_name
        vol_description = serializer.instance.vol_description
        vol_tasks = serializer.instance.vol_tasks

        normalized_name = normalize_text(vol_name)
        normalized_description = normalize_text(vol_description)
        normalized_tasks = normalize_text(vol_tasks)

        command = f'curl -H "Authorization: Bearer CDCAER5NSNNBBJHC3WHQVOHHOZTGLTLI" "https://api.wit.ai/message?v=20231202&q={normalized_name}%20{normalized_description}%20{normalized_tasks}"'

        output = subprocess.check_output(command, shell=True)

        etiqueta_ofensiva = analizar_respuesta(output)

        if etiqueta_ofensiva == 'ofensivo':
            serializer.instance.end_date = timezone.now()
            serializer.instance.has_requests = True
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

class VolunteerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]

class VolunteerSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            volunteers = Volunteer.objects.filter(
                Q(user__user_name__exact=search_param) |
                Q(user__user_email__exact=search_param)
            )

            serializer = VolunteerSerializer(volunteers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class VolunteerSearchViewbyName(generics.ListAPIView):
    serializer_class = VolunteerSerializer

    def post(self, request):
        vol_name = self.request.data.get('vol_name', '')
        #logger = logging.getLogger(__name__)
        #logger.debug("Valor de username: %s", vol_name)

        queryset = Volunteer.objects.filter(
            Q(vol_name__icontains=vol_name) &
            Q(end_date__isnull=True) &
            Q(has_requests=False)

        )
        #logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class VolunteerSearchViewbyType(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            try:
                type_id = int(search_param)
                volunteers = Volunteer.objects.filter(Q(type__type_id=type_id) | Q(type__type_name=search_param))
            except ValueError:
                volunteers = Volunteer.objects.filter(type__type_name=search_param)

            serializer = VolunteerSerializer(volunteers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class VolunteerSearchViewbyTypeUser(APIView):
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
            volunteers = Volunteer.objects.filter(query)

            serializer = VolunteerSerializer(volunteers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese al menos un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class VolunteerSearchViewbyId(generics.ListAPIView):
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        vol_id = self.request.data.get('vol_id', '')

        queryset = Volunteer.objects.filter(
            Q(vol_id__exact=vol_id)
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class VolunteerListOcultView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VolunteerSerializer

    def get_queryset(self):
        queryset = Volunteer.objects.filter(end_date__isnull=False, has_requests=True)
        return queryset


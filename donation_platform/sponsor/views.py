from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Sponsor
from .serializers import SponsorSerializer
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

class SponsorListView(generics.ListCreateAPIView):
    #queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    #permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Sponsor.objects.filter(end_date__isnull=True)
        return queryset
    def perform_create(self, serializer):
        serializer.save()

        sponsor_name = serializer.instance.sponsor_name
        sponsor_description = serializer.instance.sponsor_description

        normalized_name = normalize_text(sponsor_name)
        normalized_description = normalize_text(sponsor_description)

        command = f'curl -H "Authorization: Bearer CDCAER5NSNNBBJHC3WHQVOHHOZTGLTLI" "https://api.wit.ai/message?v=20231202&q={normalized_name}%20{normalized_description}"'

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

class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAuthenticated]

class SponsorSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            sponsors = Sponsor.objects.filter(
                Q(user__user_name__exact=search_param) |
                Q(user__user_email__exact=search_param)
            )

            serializer = SponsorSerializer(sponsors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class SponsorSearchViewbyName(generics.ListAPIView):
    serializer_class = SponsorSerializer

    def post(self, request):
        sponsor_name = self.request.data.get('sponsor_name', '')
        logger = logging.getLogger(__name__)
        logger.debug("Valor de username: %s", sponsor_name)

        queryset = Sponsor.objects.filter(
            Q(sponsor_name__icontains=sponsor_name)
        )
        logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class SponsorSearchViewbyType(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            try:
                type_id = int(search_param)
                sponsors = Sponsor.objects.filter(Q(type__type_id=type_id) | Q(type__type_name=search_param))
            except ValueError:
                sponsors = Sponsor.objects.filter(type__type_name=search_param)

            serializer = SponsorSerializer(sponsors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class SponsorSearchViewbyTypeUser(APIView):
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
            sponsors = Sponsor.objects.filter(query)

            serializer = SponsorSerializer(sponsors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese al menos un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class SponsorSearchViewbyId(generics.ListAPIView):
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sponsor_id = self.request.data.get('sponsor_id', '')

        queryset = Sponsor.objects.filter(
            Q(sponsor_id__exact=sponsor_id)
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class SponsorListOcultView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SponsorSerializer

    def get_queryset(self):
        queryset = Sponsor.objects.filter(end_date__isnull=False, has_requests=True)
        return queryset


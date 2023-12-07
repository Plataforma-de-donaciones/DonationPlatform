from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Donation
from .serializers import DonationSerializer
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

class DonationListView(generics.ListCreateAPIView):
    #queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = Donation.objects.filter(don_confirmation_date__isnull=True)
        return queryset

    #def perform_create(self, serializer):
     #   serializer.save()
    def perform_create(self, serializer):
        serializer.save()

        don_name = serializer.instance.don_name
        don_description = serializer.instance.don_description

        normalized_name = normalize_text(don_name)
        normalized_description = normalize_text(don_description)

        command = f'curl -H "Authorization: Bearer CDCAER5NSNNBBJHC3WHQVOHHOZTGLTLI" "https://api.wit.ai/message?v=20231202&q={normalized_name}%20{normalized_description}"'

        output = subprocess.check_output(command, shell=True)

        etiqueta_ofensiva = analizar_respuesta(output)

        if etiqueta_ofensiva == 'ofensivo':
            serializer.instance.don_confirmation_date = timezone.now()
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

class DonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    #def perform_destroy(self, instance):
       # Implementación de eliminación lógica
       #instance.administrator_state = 0
       #instance.erased_at = timezone.now()  # Marcar la fecha de eliminación
       #instance.save()

class DonationSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            donations = Donation.objects.filter(
                Q(user__user_name__exact=search_param) |
                Q(user__user_email__exact=search_param)
            )

            serializer = DonationSerializer(donations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class DonationSearchViewbyName(generics.ListCreateAPIView):
    serializer_class = DonationSerializer

    def post(self, request):
        don_name = self.request.data.get('don_name', '')
        logger = logging.getLogger(__name__)
        logger.debug("Valor de username: %s", don_name)

        queryset = Donation.objects.filter(
            Q(don_name__icontains=don_name)
        )
        logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class DonationSearchViewbyType(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            try:
                type_id = int(search_param)
                donations = Donation.objects.filter(Q(type__type_id=type_id) | Q(type__type_name=search_param))
            except ValueError:
                donations = Donation.objects.filter(type__type_name=search_param)

            serializer = DonationSerializer(equipments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class DonationSearchViewbyTypeUser(APIView):
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
            donations = Donation.objects.filter(query)

            serializer = DonationSerializer(donations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese al menos un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class DonationSearchViewbyId(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        don_id = self.request.data.get('don_id', '')

        queryset = Donation.objects.filter(
            Q(don_id__exact=don_id)
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class DonationListOcultView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DonationSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = Donation.objects.filter(don_confirmation_date__isnull=False, has_requests=True)
        return queryset


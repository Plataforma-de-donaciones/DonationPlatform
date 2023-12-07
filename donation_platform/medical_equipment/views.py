from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import MedicalEquipment
from .serializers import MedicalEquipmentSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
import logging
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
#from detectors import normalize_text
import subprocess
import json
import logging
import re
from unidecode import unidecode
from django.conf import settings

class MedicalEquipmentListView(generics.ListCreateAPIView):
    serializer_class = MedicalEquipmentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = MedicalEquipment.objects.filter(eq_confirmation_date__isnull=True, has_requests=False)
        return queryset
    #def perform_create(self, serializer):
     #   serializer.save()
    def perform_create(self, serializer):
        serializer.save()

        eq_name = serializer.instance.eq_name
        eq_description = serializer.instance.eq_description

        normalized_name = normalize_text(eq_name)
        normalized_description = normalize_text(eq_description)

        command = f'curl -H "Authorization: Bearer CDCAER5NSNNBBJHC3WHQVOHHOZTGLTLI" "https://api.wit.ai/message?v=20231202&q={normalized_name}%20{normalized_description}"'

        output = subprocess.check_output(command, shell=True)
        
        etiqueta_ofensiva = analizar_respuesta(output)

        if etiqueta_ofensiva == 'ofensivo':
            serializer.instance.eq_confirmation_date = timezone.now()
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

class MedicalEquipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalEquipment.objects.all()
    serializer_class = MedicalEquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class MedicalEquipmentSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            try:
                id = int(search_param)
                equipments = MedicalEquipment.objects.filter(Q(user__id=id) | Q(user__user_name=search_param) | Q(user__user_email__exact=search_param))
            except ValueError:
                equipments = MedicalEquipment.objects.filter( Q(user__user_name=search_param) | Q(user__user_email__exact=search_param))

            serializer = MedicalEquipmentSerializer(equipments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class MedicalEquipmentSearchViewbyName(generics.ListCreateAPIView):
    serializer_class = MedicalEquipmentSerializer
    #parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        eq_name = self.request.data.get('eq_name', '')
        queryset = MedicalEquipment.objects.filter(
            Q(eq_name__icontains=eq_name) &
            Q(eq_confirmation_date__isnull=True) &
            Q(has_requests=False)
        )
        #serializer = self.serializer_class(queryset, many=True)
        #return Response(serializer.data)
        serialized_data = self.serializer_class(queryset, many=True).data
        for item in serialized_data:
            item['eq_attachment'] = settings.SERVER_URL + item['eq_attachment']

        return Response(serialized_data)

class MedicalEquipmentSearchViewbyType(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            try:
                type_id = int(search_param)
                equipments = MedicalEquipment.objects.filter(Q(type__type_id=type_id) | Q(type__type_name=search_param))
            except ValueError:
                equipments = MedicalEquipment.objects.filter(type__type_name=search_param)
            serializer = MedicalEquipmentSerializer(equipments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class MedicalEquipmentSearchViewbyTypeUser(APIView):
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
            equipments = MedicalEquipment.objects.filter(query)

            serializer = MedicalEquipmentSerializer(equipments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese al menos un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class MedicalEquipmentSearchViewbyId(generics.ListAPIView):
    serializer_class = MedicalEquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        eq_id = self.request.data.get('eq_id', '')

        queryset = MedicalEquipment.objects.filter(
            Q(eq_id__exact=eq_id)
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class MedicalEquipmentSearchViewbyNames(generics.ListAPIView):
    serializer_class = MedicalEquipmentSerializer

    def post(self, request):
        eq_name = self.request.data.get('eq_name', '')

        queryset = MedicalEquipment.objects.filter(
            Q(eq_name__icontains=eq_name) &
            Q(eq_confirmation_date__isnull=True) &
            Q(type=2)
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class MedicalEquipmentListOcultView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MedicalEquipmentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = MedicalEquipment.objects.filter(eq_confirmation_date__isnull=False, has_requests=True)
        return queryset


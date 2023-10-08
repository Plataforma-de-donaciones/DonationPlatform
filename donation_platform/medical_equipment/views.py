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

class MedicalEquipmentListView(generics.ListCreateAPIView):
    queryset = MedicalEquipment.objects.all()
    serializer_class = MedicalEquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class MedicalEquipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalEquipment.objects.all()
    serializer_class = MedicalEquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    #def perform_destroy(self, instance):
       # Implementación de eliminación lógica
       #instance.administrator_state = 0
       #instance.erased_at = timezone.now()  # Marcar la fecha de eliminación
       #instance.save()

class MedicalEquipmentSearchViewbyUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            try:
                id = int(search_param)
                equipments = MedicalEquipment.objects.filter(Q(user__id=id) | Q(user__user_name=search_param) | Q(user__user_email__exact=search_param))
            except ValueError:
                # Si no es un número, busca por type_name
                equipments = MedicalEquipment.objects.filter( Q(user__user_name=search_param) | Q(user__user_email__exact=search_param))

            serializer = MedicalEquipmentSerializer(equipments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class MedicalEquipmentSearchViewbyName(generics.ListAPIView):
    serializer_class = MedicalEquipmentSerializer

    def post(self, request):
        eq_name = self.request.data.get('eq_name', '')
        logger = logging.getLogger(__name__)
        logger.debug("Valor de username: %s", eq_name)

        queryset = MedicalEquipment.objects.filter(
            Q(eq_name__icontains=eq_name)
        )
        logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class MedicalEquipmentSearchViewbyType(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            # Intenta buscar por type_id como número
            try:
                type_id = int(search_param)
                equipments = MedicalEquipment.objects.filter(Q(type__type_id=type_id) | Q(type__type_name=search_param))
            except ValueError:
                # Si no es un número, busca por type_name
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
            # Configura la consulta usando Q para manejar ambas condiciones
            query = Q()

            if search_type_param:
                query &= (Q(type__type_name__exact=search_type_param) | Q(type__type_id=search_type_param))

            if search_user_param:
                query &= (Q(user__user_name__exact=search_user_param) | Q(user__user_email__exact=search_user_param))

            # Ejecuta la consulta
            equipments = MedicalEquipment.objects.filter(query)

            serializer = MedicalEquipmentSerializer(equipments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese al menos un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

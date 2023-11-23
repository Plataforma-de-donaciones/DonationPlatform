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

class VolunteerListView(generics.ListCreateAPIView):
    #queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Volunteer.objects.filter(end_date__isnull=True)
        return queryset

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
        logger = logging.getLogger(__name__)
        logger.debug("Valor de username: %s", vol_name)

        queryset = Volunteer.objects.filter(
            Q(vol_name__icontains=vol_name)
        )
        logger.debug("Consulta sql generada:", str(queryset.query))
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
                # Si no es un número, busca por type_name
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
            # Configura la consulta usando Q para manejar ambas condiciones
            query = Q()

            if search_type_param:
                query &= (Q(type__type_name__exact=search_type_param) | Q(type__type_id=search_type_param))

            if search_user_param:
                query &= (Q(user__user_name__exact=search_user_param) | Q(user__user_email__exact=search_user_param))

            # Ejecuta la consulta
            volunteers = Volunteer.objects.filter(query)

            serializer = VolunteerSerializer(volunteers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese al menos un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class VolunteerSearchViewbyId(generics.ListAPIView):
    serializer_class = VolunteerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        vol_id = self.request.data.get('vol_id', '')
        #logger = logging.getLogger(__name__)
        #logger.debug("Valor de username: %s", eq_name)

        queryset = Volunteer.objects.filter(
            Q(vol_id__exact=vol_id)
        )
        #logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


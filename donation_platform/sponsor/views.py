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

class SponsorListView(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAuthenticated]

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
            # Configura la consulta usando Q para manejar ambas condiciones
            query = Q()

            if search_type_param:
                query &= (Q(type__type_name__exact=search_type_param) | Q(type__type_id=search_type_param))

            if search_user_param:
                query &= (Q(user__user_name__exact=search_user_param) | Q(user__user_email__exact=search_user_param))

            # Ejecuta la consulta
            sponsors = Sponsor.objects.filter(query)

            serializer = SponsorSerializer(sponsors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese al menos un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class SponsorSearchViewbyId(generics.ListAPIView):
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sponsor_id = self.request.data.get('sponsor_id', '')
        #logger = logging.getLogger(__name__)
        #logger.debug("Valor de username: %s", eq_name)

        queryset = Sponsor.objects.filter(
            Q(sponsor_id__exact=sponsor_id)
        )
        #logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


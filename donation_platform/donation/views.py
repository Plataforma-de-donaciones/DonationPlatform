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

class DonationListView(generics.ListCreateAPIView):
    #queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = Donation.objects.filter(don_confirmation_date__isnull=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save()

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

class DonationSearchViewbyName(generics.ListAPIView):
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

#class DonationSearchViewbyType(generics.ListAPIView):
#    serializer_class = DonationSerializer
#    permission_classes = [permissions.IsAuthenticated]

#    def get_queryset(self):
 #       queryset = Donation.objects.all()
#
 #       if self.request.method == 'POST':
  #          search_param = self.request.data.get('search', None)
#
 #           if search_param:
  #              queryset = queryset.filter(
   #                 Q(type__type_name__icontains=search_param)
    #            )
#
 #       return queryset

#class DonationSearchViewbyType(APIView):
 #   permission_classes = [permissions.IsAuthenticated]
#
 #   def post(self, request):
  #      search_param = request.data.get('search', '')

   #     if search_param:
    #        donations = Donation.objects.filter(
     #           Q(type__type_name__exact=search_param)
      #      )
#
 #           serializer = DonationSerializer(donations, many=True)
  #          return Response(serializer.data, status=status.HTTP_200_OK)

   #     return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class DonationSearchViewbyType(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            # Intenta buscar por type_id como número
            try:
                type_id = int(search_param)
                donations = Donation.objects.filter(Q(type__type_id=type_id) | Q(type__type_name=search_param))
            except ValueError:
                # Si no es un número, busca por type_name
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
            # Configura la consulta usando Q para manejar ambas condiciones
            query = Q()

            if search_type_param:
                query &= (Q(type__type_name__exact=search_type_param) | Q(type__type_id=search_type_param))

            if search_user_param:
                query &= (Q(user__user_name__exact=search_user_param) | Q(user__user_email__exact=search_user_param))

            # Ejecuta la consulta
            donations = Donation.objects.filter(query)

            serializer = DonationSerializer(donations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese al menos un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

class DonationSearchViewbyId(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        don_id = self.request.data.get('don_id', '')
        #logger = logging.getLogger(__name__)
        #logger.debug("Valor de username: %s", eq_name)

        queryset = Donation.objects.filter(
            Q(don_id__exact=don_id)
        )
        #logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


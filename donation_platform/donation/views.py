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

class DonationListView(generics.ListCreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

class DonationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    #def perform_destroy(self, instance):
       # Implementación de eliminación lógica
       #instance.administrator_state = 0
       #instance.erased_at = timezone.now()  # Marcar la fecha de eliminación
       #instance.save()

class DonationSearchViewbyUser(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Donation.objects.all()
        
        if self.request.method == 'POST':
            search_param = self.request.data.get('search', None)

            if search_param:
                queryset = queryset.filter(
                    Q(user__user_name__icontains=search_param)
                )

        return queryset

class DonationSearchViewbyName(generics.ListAPIView):
    serializer_class = DonationSerializer

    def post(self, request):
        don_name = self.request.data.get('don_name', '')
        logger = logging.getLogger(__name__)
        logger.debug("Valor de username: %s", don_name)

        queryset = Donation.objects.filter(
            Q(user_name__exact=don_name)
        )
        logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class DonationSearchViewbyType(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Donation.objects.all()

        if self.request.method == 'POST':
            search_param = self.request.data.get('search', None)

            if search_param:
                queryset = queryset.filter(
                    Q(type__type_name__icontains=search_param)
                )

        return queryset


from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Organization
from .serializers import OrganizationSerializer
from django.utils import timezone
from rest_framework.response import Response

class OrganizationListView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrganizationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrganizationSearchView(generics.ListAPIView):
    serializer_class = OrganizationSerializer

    def post(self, request):
        org_name = self.request.data.get('org_name', '')
        org_email = self.request.data.get('org_email', '')

        queryset = Organization.objects.filter(
            Q(org_name__exact=org_name) | Q(org_email__exact=org_email)
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


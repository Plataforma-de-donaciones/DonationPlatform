from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Administrator
from .serializers import AdministratorSerializer
from django.utils import timezone

class AdministratorListView(generics.ListCreateAPIView):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer
    permission_classes = [permissions.IsAuthenticated]

class AdministratorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
       # Implementación de eliminación lógica
       instance.administrator_state = 0
       instance.erased_at = timezone.now()  # Marcar la fecha de eliminación
       instance.save()

class AdministratorSearchView(generics.ListAPIView):
    serializer_class = AdministratorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Administrator.objects.all()
        
        if self.request.method == 'POST':
            search_param = self.request.data.get('search', None)

            if search_param:
                queryset = queryset.filter(
                    Q(user__user_name__icontains=search_param) |
                    Q(user__user_email__icontains=search_param)
                )

        return queryset


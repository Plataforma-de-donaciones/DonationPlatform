from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Moderator
from .serializers import ModeratorSerializer
from django.utils import timezone


class ModeratorListView(generics.ListCreateAPIView):
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSerializer
    permission_classes = [permissions.IsAuthenticated]

class ModeratorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
       # Implementación de eliminación lógica
       instance.moderator_state = 0
       instance.erased_at = timezone.now()  # Marcar la fecha de eliminación
       instance.save()

class ModeratorSearchView(generics.ListAPIView):
    serializer_class = ModeratorSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = Moderator.objects.all()
        search_param = self.request.data.get('search', None)

        if search_param:
            queryset = queryset.filter(
                Q(user__user_name__icontains=search_param) |
                Q(user__user_email__icontains=search_param)
            )

        return queryset

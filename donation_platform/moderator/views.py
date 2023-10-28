from django.shortcuts import render
from rest_framework import generics, permissions, status
from django.db.models import Q
from .models import Moderator
from .serializers import ModeratorSerializer
from django.utils import timezone
from rest_framework.response import Response
from users.models import Users
from rest_framework.views import APIView

class ModeratorListView(generics.ListCreateAPIView):
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSerializer
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        start_date = request.data.get('start_date')
        organization_id = request.data.get('organization_id')
        moderator_state = request.data.get('moderator_state')

        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response({'message': 'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)

        if user.user_state != 1:
            return Response({'message': 'El usuario debe estar activo para crear un moderador'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ModeratorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
       # Implementación de eliminación lógica
       instance.moderator_state = 0
       instance.erased_at = timezone.now()  # Marcar la fecha de eliminación
       instance.save()

#class ModeratorSearchView(generics.ListAPIView):
#    serializer_class = ModeratorSerializer
#    permission_classes = [permissions.IsAuthenticated]
#    http_method_names = ['get', 'post']

#    def get_queryset(self):
#        queryset = Moderator.objects.all()
#        search_param = self.request.data.get('search', None)

#        if search_param:
#            queryset = queryset.filter(
#                Q(user__user_name__icontains=search_param) |
#                Q(user__user_email__icontains=search_param)
#            )
#
#        return queryset

class ModeratorSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            moderators = Moderator.objects.filter(
                Q(user__user_name__icontains=search_param) |
                Q(user__user_email__icontains=search_param)
            )

            serializer = ModeratorSerializer(moderators, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

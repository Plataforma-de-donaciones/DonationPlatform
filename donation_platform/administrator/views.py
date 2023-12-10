from django.shortcuts import render
from rest_framework import generics, permissions, status
from django.db.models import Q
from .models import Administrator
from .serializers import AdministratorSerializer
from django.utils import timezone
from users.models import Users
from rest_framework.response import Response
from rest_framework.views import APIView

class AdministratorListView(generics.ListCreateAPIView):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        data_with_user_info = []
        for administrator_data in response.data:
            user_id = administrator_data.get('user')
            try:
                user = Users.objects.get(id=user_id)
                user_info = {
                    'user_id': user.id,
                    'user_name': user.user_name,
                    'user_email': user.user_email,
                }
                administrator_data['user_info'] = user_info
            except Users.DoesNotExist:
                administrator_data['user_info'] = None

            data_with_user_info.append(administrator_data)

        response.data = data_with_user_info
        return response

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        start_date = request.data.get('start_date')
        organization_id = request.data.get('organization_id')
        administrator_state = request.data.get('administrator_state')

        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response({'message': 'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)

        if user.user_state != 1:
            return Response({'message': 'El usuario debe estar activo para crear un administrador'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AdministratorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
       instance.administrator_state = 0
       instance.erased_at = timezone.now()
       instance.save()

class AdministratorSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_param = request.data.get('search', '')

        if search_param:
            administrators = Administrator.objects.filter(
                Q(user__user_name__icontains=search_param) |
                Q(user__user_email__icontains=search_param)
            )

            serializer = AdministratorSerializer(administrators, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Ingrese un parámetro de búsqueda válido.'}, status=status.HTTP_400_BAD_REQUEST)

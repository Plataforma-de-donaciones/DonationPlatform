from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Users
from .serializers import UsersSerializer, UsersSimpleSerializer
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import logging
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
import json
from django.http import JsonResponse
#from django.views.decorators.csrf import ensure_csrf_cookie
#from django.views.decorators.csrf import csrf_exempt
from .models import Administrator, Moderator
#from donation_platform.permissions import UsuarioClusterPermiso

class UsersListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

class UsersCreateView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        plain_password = self.request.data.get('user_password', '')
        hashed_password = make_password(plain_password)

        request.data['user_password'] = hashed_password

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UsersDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
       instance.user_state = 0
       instance.erased_at = timezone.now()
       instance.save()
    def perform_update(self, serializer):
        plain_password = self.request.data.get('user_password', '')
        hashed_password = make_password(plain_password)
        serializer.validated_data['user_password'] = hashed_password

        super().perform_update(serializer)

class UserSearchView(generics.ListAPIView):
    serializer_class = UsersSerializer

    def post(self, request):
        user_name = self.request.data.get('user_name', '')
        user_email = self.request.data.get('user_email', '')
        
        logger = logging.getLogger(__name__)
        logger.debug("Valor de username: %s", user_name)
        logger.debug("Valor de email: %s", user_email)
       
        queryset = Users.objects.filter(
            Q(user_name__exact=user_name) | Q(user_email__exact=user_email)
        )
        logger.debug("Consulta sql generada:", str(queryset.query))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class UserLoginView(APIView):
    def post(self, request):
        user_name = request.data.get('user_name')
        user_password = request.data.get('user_password')

        try:
            user = Users.objects.get(user_name=user_name)
        except Users.DoesNotExist:
            user = None

        if user is not None and check_password(user_password, user.user_password) and user.user_state == 1:
            login(request, user)

            token, created = Token.objects.get_or_create(user=user)

            user_data = {
                'user_id': user.id,
                'user_email': user.user_email,
            }
            return JsonResponse({'message': 'Inicio de sesión exitoso', 'token': token.key, 'user_data': user_data})
        else:
            return JsonResponse({'message': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class UserRoleView(APIView):
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = self.request.data.get('id', '')

        administrator = Administrator.objects.filter(user=user_id, administrator_state=1).first()
        if administrator:
            return JsonResponse({"user_role": "administrator"})

        moderator = Moderator.objects.filter(user=user_id, moderator_state=1).first()
        if moderator:
            return JsonResponse({"user_role": "moderator"})

        return JsonResponse({"user_role": "user"})

class UserSearchViewbyId(generics.ListAPIView):
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        id = self.request.data.get('id', '')
        

        queryset = Users.objects.filter(
            Q(id__exact=id)
        )
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class UsersLoginView(APIView):
    
    serializer_class = UsersSimpleSerializer

    def post(self, request):
        user_name = request.data.get('user_name')
        user_password = request.data.get('user_password')

        try:
            user = Users.objects.get(user_name=user_name)
        except Users.DoesNotExist:
            user = None


        if user is not None and check_password(user_password, user.user_password) and user.user_state == 1:

            login(request, user)
            
            existing_token = Token.objects.filter(user=user).first()
            if existing_token:
                existing_token.delete()
            new_token = Token.objects.create(user=user)
           

            return Response({'message': 'Inicio de sesión exitoso', 'token': new_token.key})

        else:
            return JsonResponse({'message': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


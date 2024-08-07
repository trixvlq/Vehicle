import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.conf import settings
from datetime import datetime, timedelta, timezone

from api.permission import TokenPermission
from .serializers import LoginSerializer, RegistrationSerializer, User
from .token_services import validate_token

import environ

env = environ.Env()
environ.Env.read_env()


class LoginView(APIView):
    """
    API view для аутентификации пользователя.

    Пользователи могут войти в систему с помощью логина и пароля.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Обрабатывает POST запрос для аутентификации пользователя.

        Аргументы:
            request: объект запроса, содержащий логин и пароль пользователя.

        Возвращает:
            Response: результат выполнения запроса, включая обновленный токен, если требуется.
        """
        if validate_token(request):
            return Response({"message": "Already logged in"}, status=409)
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']
        password = serializer.data['password']

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials')

        payload = {
            'id': user.id,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=60),
            'iat': datetime.now(timezone.utc)
        }
        refresh_payload = {
            'id': user.id,
            'exp': datetime.now(timezone.utc) + timedelta(days=1),
            'iat': datetime.now(timezone.utc)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithms=[env('ALGORITHM')])
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithms=[env('ALGORITHM')])
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.set_cookie(key='refresh', value=refresh_token, httponly=True)

        response.data = {
            'status': 'success'
        }
        return response


class RegistrationView(APIView):
    """
    API view для регистрации нового пользователя.

    Пользователи могут зарегистрироваться с помощью логина и пароля.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Обрабатывает POST запрос для регистрации нового пользователя.

        Аргументы:
            request: объект запроса, содержащий логин и пароль пользователя.

        Возвращает:
            Response: результат выполнения запроса, включая обновленный токен, если требуется.
        """
        if validate_token(request):
            return Response({"message": "Already logged in"}, status=409)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LogoutView(APIView):
    """
    API view для выхода пользователя из системы.

    Пользователи могут выйти из системы, используя обновленный токен.
    """
    permission_classes = (TokenPermission,)

    def post(self, request):
        """
        Обрабатывает POST запрос для выхода пользователя из системы.

        Аргументы:
            request: объект запроса, содержащий обновленный токен пользователя.

        Возвращает:
            Response: результат выполнения запроса, включая обновленный токен, если требуется.
        """
        response = Response()
        response.delete_cookie(key='jwt')
        response.delete_cookie(key='refresh')
        response.data = {
            'status': 'success'
        }
        return response

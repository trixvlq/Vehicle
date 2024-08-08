from rest_framework.permissions import BasePermission
from django.conf import settings
import jwt
from datetime import datetime, timedelta, timezone
from users.token_services import check_token
import environ

env = environ.Env()
environ.Env.read_env()

class TokenPermission(BasePermission):
    """
    Разрешение для проверки токенов JWT.

    Проверяет наличие действительного токена JWT в куках запроса и при необходимости обновляет его.
    """

    def has_permission(self, request, view):
        """
        Проверяет, имеет ли запрос разрешение на доступ к ресурсу.

        Проверяет наличие токена JWT и его действительность. Если токен недействителен,
        проверяет refresh-токен и обновляет основной токен, если refresh-токен действителен.

        Аргументы:
            request: объект запроса, содержащий токены в куках.
            view: текущий view (не используется в этой реализации).

        Возвращает:
            bool: True, если токен действителен или был успешно обновлен, иначе False.
        """
        token = request.COOKIES.get('jwt')
        refresh = request.COOKIES.get('refresh')

        if token and check_token(token):
            return True

        if refresh and check_token(refresh):
            try:
                new_payload = jwt.decode(refresh, settings.SECRET_KEY, algorithm=env('ALGORITHM'))
                new_payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=60)
                new_token = jwt.encode(new_payload, settings.SECRET_KEY, algorithm=env('ALGORITHM'))
                request.new_token = new_token
                return True
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return False

        return False

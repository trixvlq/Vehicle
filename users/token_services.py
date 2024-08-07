import jwt
from django.conf import settings
import environ

env = environ.Env()
environ.Env.read_env()


def check_token(token):
    """
    Проверяет, действителен ли токен.

    Аргументы:
        token (str): JWT токен для проверки.

    Возвращает:
        dict или False: Расшифрованная полезная нагрузка токена, если он действителен; иначе False.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[env('ALGORITHM')])
    except jwt.ExpiredSignatureError:
        return False
    return payload


def validate_token(request):
    """
    Проверяет наличие и действительность токена в запросе.

    Если основной токен недействителен, проверяет refresh-токен и обновляет основной токен.

    Аргументы:
        request: объект запроса, содержащий токены в куках.

    Возвращает:
        str или False: Обновленный основной токен, если refresh-токен действителен; иначе False.
    """
    token = request.COOKIES.get('jwt')
    refresh = request.COOKIES.get('refresh')
    if not token and not refresh:
        return False
    if check_token(token):
        return token
    else:
        if check_token(refresh):
            token = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[env('ALGORITHM')])
            token = jwt.encode(token, settings.SECRET_KEY, algorithm=[env('ALGORITHM')])
            return token
    return False

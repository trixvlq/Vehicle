from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from vehicles.filters import CarFilter
from vehicles.models import Car, fuel_types, gear_types
from vehicles.pagination import CarPaginator
from vehicles.serializers import CarSerializer
from api.permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CarListAddView(generics.ListCreateAPIView):
    """
    API view для получения списка автомобилей и добавления нового автомобиля.

    Пользователи могут фильтровать автомобили по различным параметрам и создавать новые записи.
    """
    permission_classes = (TokenPermission,)
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarFilter
    pagination_class = CarPaginator

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'brand': openapi.Schema(type=openapi.TYPE_STRING),
                'model': openapi.Schema(type=openapi.TYPE_STRING),
                'year_made': openapi.Schema(type=openapi.TYPE_INTEGER),
                'fuel': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=[choice[0] for choice in fuel_types],
                    description='Possible values: ' + ', '.join([choice[0] for choice in fuel_types])
                ),
                'gear': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=[choice[0] for choice in gear_types],
                    description='Possible values: ' + ', '.join([choice[0] for choice in gear_types])
                ),
                'mileage': openapi.Schema(type=openapi.TYPE_INTEGER),
                'price': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        )
    )
    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST запрос для создания нового автомобиля.

        Аргументы:
            request: объект запроса, содержащий данные автомобиля для создания.

        Возвращает:
            Response: результат выполнения запроса, включая ошибки валидации, если таковые имеются.
        """
        try:
            return super().post(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def get(self, request):
        """
        Обрабатывает GET запрос для получения списка автомобилей с фильтрацией и пагинацией.

        Аргументы:
            request: объект запроса.

        Возвращает:
            Response: результат выполнения запроса, включая обновленный токен, если требуется.
        """
        try:
            if hasattr(request, 'new_token'):
                response = Response({'message': 'Token refreshed'})
                response.set_cookie('jwt', request.new_token)
                return response
            return super().get(request)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view для получения информации об автомобиле, его обновления и его удаления.

    Пользователи могут получать информацию об автомобиле, обновлять его и удалять самостоятельно.
    """
    permission_classes = (TokenPermission,)
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET запрос для получения информации об автомобиле.

        Аргументы:
            id: идентификатор автомобиля.

        Возвращает:
            Response: результат выполнения запроса, включая обновленный токен, если требуется.
        """
        try:
            if hasattr(request, 'new_token'):
                response = Response({'message': 'Token refreshed'})
                response.set_cookie('jwt', request.new_token)
                return response
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

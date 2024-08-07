import django_filters
from vehicles.models import Car


class CarFilter(django_filters.FilterSet):
    """
    Фильтр для модели Car.

    Позволяет фильтровать автомобили по различным параметрам, таким как пробег и цена.
    """
    min_mileage = django_filters.NumberFilter(field_name='mileage', lookup_expr='gte')
    max_mileage = django_filters.NumberFilter(field_name='mileage', lookup_expr='lte')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Car
        fields = ['brand', 'model', 'year_made', 'fuel', 'gear', 'min_mileage', 'max_mileage', 'min_price', 'max_price']


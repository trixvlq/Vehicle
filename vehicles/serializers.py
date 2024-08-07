from .models import Car, fuel_types, gear_types
from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Car
    """

    class Meta:
        model = Car
        fields = '__all__'

    def validate_fuel(self, value):
        """
        Проверка на валидность типа топлива

        Аргументы:
            value (str): тип топлива

        Результат:
            value (str): тип топлива либо ошибка валидации
        """
        if value not in dict(fuel_types).keys():
            raise serializers.ValidationError(
                f'Invalid fuel type. Possible values are: {", ".join(dict(fuel_types).keys())},',
            )
        return value

    def validate_gear(self, value):
        """
        Проверка на валидность типа двигателя

        Аргументы:
            value (str): тип двигателя

        Результат:
            value (str): тип двигателя либо ошибка валидации
        """
        if value not in dict(gear_types).keys():
            raise serializers.ValidationError(
                f'Invalid gear type. Possible values are: {", ".join(dict(gear_types).keys())}'
            )
        return value

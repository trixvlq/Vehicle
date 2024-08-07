from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

fuel_types = [('Бензин', 'Бензин'), ('Дизель', 'Дизель'), ('Электро', 'Электро'), ('Гибрид', 'Гибрид')]
gear_types = [('Механика', 'Механика'), ('Автомат', 'Автомат'), ('Робот', 'Робот'), ('Вариатор', 'Вариатор')]


class Car(models.Model):
    """
    Модель автомобиля

    brand - марка(string)
    model - модель(string)
    year_made - год выпуска(int)
    fuel - тип топлива(string)
    gear - тип привода(string)
    mileage - пробег(int)
    price - цена(int)
    """
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year_made = models.IntegerField(validators=(MinValueValidator(1672), MaxValueValidator(2024)))
    fuel = models.CharField(max_length=100, choices=fuel_types)
    gear = models.CharField(max_length=100, choices=gear_types)
    mileage = models.IntegerField(validators=(MinValueValidator(0),))
    price = models.IntegerField(validators=(MinValueValidator(0),))

    def __str__(self):
        return self.model

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя
    """
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        '''
        Функция для создания пользователя

        Аргументы:
            validated_data: словарь с данными пользователя

        Возвращает:
            User: созданный пользователь
        '''
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_username(self, value):
        """
        Функция для проверки уникальности имени пользователя

        Аргументы:
            value: имя пользователя

        Возвращает:
            User: проверенное имя пользователя
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('User with this username already exists')
        return value

    def validate_password(self, value):
        """
        Функция для проверки длины пароля пользователя

        Аргументы:
            value: пароль пользователя

        Возвращает:
            User: проверенное пароль пользователя
        """
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        return value


class LoginSerializer(serializers.Serializer):
    '''
    Сериализатор для входа в систему
    '''
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

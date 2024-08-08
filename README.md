# Проект по управлению автомобилями

## Стек технологий

<img src="https://img.shields.io/badge/Python-4169E1?style=for-the-badge"/> 
<img src="https://img.shields.io/badge/Django-008000?style=for-the-badge"/> 
<img src="https://img.shields.io/badge/DRF-800000?style=for-the-badge"/> 
<img src="https://img.shields.io/badge/Docker-00BFFF?style=for-the-badge"/> 
<img src="https://img.shields.io/badge/PostgreSQL-87CEEB?style=for-the-badge"/>
<img src="https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white"/>


## Описание проекта

Этот проект представляет собой систему управления данными автомобилей. Он включает в себя создание, чтение, обновление и
удаление (CRUD) записей об автомобилях, а также поддержку фильтрации по различным параметрам. Система реализована с
использованием Django и Django REST Framework для API, PostgreSQL для хранения данных, и Docker для контейнеризации.

Проект включает следующие функции:

- Создание записи об автомобиле
- Чтение данных об автомобилях
- Обновление информации об автомобилях
- Удаление записей об автомобилях
- Фильтрация автомобилей по параметрам (марка, модель, год и т.д.)
- Пагинация результатов
- Аутентификация и авторизация пользователей
- Документация API через Swagger

## Как запустить проект

1. Клонировать репозиторий:

   ```bash
   git clone https://github.com/trixvlq/Vehicle.git
   ```
   
2. Перейти в папку с проектом:

   ```bash
   cd Vehicle
   ```

3.  Создать файл `.env` в директории `backend` и задать следующие переменные:

   ```plaintext
   ALG=HS256
   SECRET_KEY=django-insecure-...
   DEBUG=True
   DB_HOST=mega_db(название контейнера с бд)
   DB_NAME=your_db_name(postgres)
   DB_USER=your_db_user(postgres)
   DB_PASSWORD=your_db_password(postgres)
   ```
Файл уже создан, по желанию его можно изменить

4. Построить Docker контейнер:

   ```bash
   docker-compose build
   ```

5. Запустить контейнер:

   ```bash
   docker-compose up
   ```

   Теперь проект доступен по адресу: `http://127.0.0.1/`.

## Документация API

### Базовый URL

```
http://127.0.0.1/api/v1/
```

### Эндпоинты

#### Создание автомобиля

**URL:** `/v1/cars/`  
**Метод:** `POST`  
**Описание:** Создает новый автомобиль.  
**Данные запроса:**

- `make` (строка) — Марка автомобиля
- `model` (строка) — Модель автомобиля
- `year` (целое число) — Год выпуска
- `color` (строка) — Цвет

**Ответ:**

- **201 Created:** Сериализованные данные созданного автомобиля.
- **400 Bad Request:** Неверные данные запроса.

#### Получение данных об автомобиле

**URL:** `/v1/cars/{id}/`  
**Метод:** `GET`  
**Описание:** Возвращает данные об автомобиле по его ID.  
**Ответ:**

- **200 OK:** Сериализованные данные автомобиля.
- **404 Not Found:** Автомобиль не найден.

#### Обновление данных об автомобиле

**URL:** `/v1/cars/{id}/`  
**Метод:** `PUT`  
**Описание:** Обновляет информацию об автомобиле по его ID.  
**Данные запроса (опционально):**

- `make` (строка) — Марка автомобиля
- `model` (строка) — Модель автомобиля
- `year` (целое число) — Год выпуска
- `color` (строка) — Цвет

**Ответ:**

- **200 OK:** Обновленные данные автомобиля.
- **400 Bad Request:** Неверные данные запроса.
- **404 Not Found:** Автомобиль не найден.

#### Удаление автомобиля

**URL:** `/v1/cars/{id}/`  
**Метод:** `DELETE`  
**Описание:** Удаляет автомобиль по его ID.  
**Ответ:**

- **204 No Content:** Удаление успешно.
- **404 Not Found:** Автомобиль не найден.

#### Фильтрация автомобилей

**URL:** `/v1/cars/`  
**Метод:** `GET`  
**Описание:** Возвращает список автомобилей с возможностью фильтрации и пагинации.  
**Параметры запроса (query params):**

- `make` (строка) — Фильтр по марке
- `model` (строка) — Фильтр по модели
- `year` (целое число) — Фильтр по году выпуска
- `color` (строка) — Фильтр по цвету
- `page` (целое число) — Номер страницы для пагинации
- `page_size` (целое число) — Количество элементов на странице

**Ответ:**

- **200 OK:** Список сериализованных данных автомобилей.

## Примечания по использованию

- **Аутентификация:** Некоторые эндпоинты могут требовать аутентификацию. Убедитесь, что JWT-токены правильно настроены
  и передаются в заголовках запросов или в cookies.
- **Документация:** Полная документация API доступна через Swagger по адресу: `http://127.0.0.1/swagger/`.

## Примеры запросов

#### Создание автомобиля

**Запрос:**

```json
{
  "make": "Toyota",
  "model": "Camry",
  "year": 2022,
  "color": "White"
}
```

**Ответ:**

```json
{
  "id": 1,
  "make": "Toyota",
  "model": "Camry",
  "year": 2022,
  "color": "White"
}
```

#### Получение данных об автомобиле

**Запрос:**

```http
GET /v1/cars/1/
```

**Ответ:**

```json
{
  "id": 1,
  "make": "Toyota",
  "model": "Camry",
  "year": 2022,
  "color": "White"
}
```

#### Фильтрация автомобилей

**Запрос:**

```http
GET /v1/cars/?make=Toyota&year=2022&page=1&page_size=10
```

**Ответ:**

```json
[
  {
    "id": 1,
    "make": "Toyota",
    "model": "Camry",
    "year": 2022,
    "color": "White"
  }
]
```

## Автор

- Имя: Цзю Максим
- Email: qwefghnz@gmail.com
- GitHub: [trixvlq](https://github.com/trixvlq)

Эта структура включает все необходимые детали и полезные примеры, которые помогут пользователям понять, как использовать
ваше API и запустить проект.

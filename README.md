# Начало знакомства с api

## Запуск контейнера 
- Внимательно прочитать .env.example
- Создать .env.prod
- запустить одной командой из корня проекта

##### Команда запуска
```bash
docker-compose up --build 
```
###### Больше ничего не нужно делать, миграции будут применены база данных будет заполнена фикстурой сама

---
## Запуск без контейнера
### Для настроек проекта нужно использовать переменные окружения

###### пример файла .env

```
.env.example
```
---
### Установить все зависимости

```python
pip install - r requirements.txt
```
---
### Применить все миграции

```python
python manage.py migrate 
```
---
### Создать админа

```python
python manage.py admin_reg
```


###### Файл для создания админа находится по пути

###### users/management/commands/admin_reg.py

---
### Запуск сервера

```python
python manage.py runserver 
```
---
### Создание случайных курсов и уроков 

```python
python manage.py load_data --num_courses 5 --num_lessons 4
```

###### ***--num_courses*** кол-во курсов, по умолчанию 3
######  
###### ***--num_lessons*** кол-во уроков в курсе, по умолчанию 3

---

### Загрузка фикстуры БД
```python
python manage.py loaddata db.json  
```

---


## Пользователи в базе

> username-> ***admin@example.com***
>
>password-> ***admin***

> username-> ***kosta123139@gmail.com***
>
>password-> ***Hh14767Hh***

> username-> ***john.doe@example.com***
>
>password-> ***Hh14767Hh***

#
# Документация API

###### также есть и http://localhost:8000/swagger/

---
## Аутентификация

### Регистрация пользователя
- **POST** `/api/register/`
  - Регистрация нового пользователя.


### Профиль пользователя
- **GET** `/api/profile/`
  - Информация о профиле.

- **PUT** `/api/profile/{id}/`
  - Обновление информации профиля.

- **DELETE** `/api/profile/{id}/`
  - Деактивация профиля пользователя.


### Управление токенами
- **POST** `/api/token/`
  - Получение новой пары токенов (доступа и обновления).
  
- **POST** `/api/token-refresh/`
  - Обновление токена доступа с использованием токена обновления.
---
## Курсы

### Управление курсами
- **GET** `/api/courses/`
  - Получение списка всех курсов (для модераторов) или курсов пользователя.

- **POST** `/api/courses/`
  - Создание нового курса (доступно модераторам и авторам курсов).

- **GET** `/api/courses/{id}/`
  - Получение конкретного курса по ID.

- **PUT** `/api/courses/{id}/`
  - Обновление конкретного курса по ID (доступно модераторам и авторам курсов).

- **DELETE** `/api/courses/{id}/`
  - Удаление конкретного курса по ID (доступно только авторам курсов).
---
## Уроки

### Управление уроками
- **GET** `/api/lessons/`
  - Получение списка всех уроков (для модераторов) или уроков пользователя.

- **POST** `/api/lessons/`
  - Создание нового урока (доступно модераторам и авторам уроков).

- **GET** `/api/lessons/{id}/`
  - Получение конкретного урока по ID.

- **PUT** `/api/lessons/{id}/`
  - Обновление конкретного урока по ID (доступно модераторам и авторам уроков).

- **DELETE** `/api/lessons/{id}/`
  - Удаление конкретного урока по ID (доступно только авторам уроков).
---

## Подписка

### Управление подписками
- **GET** `/api/subscribe/`
  - Получение списка всех подписок пользователя.

- **POST** `/api/subscribe/`
  - подписаться на курс.
  - передать id курса `{"id":id}`.

- **DELETE** `/api/subscribe/`
  - Удаление подписки.
  - передать id курса `{"id":id}`.
---

## Платежи

### Управление платежами
- **GET** `/api/payments/`
  - Получение списка всех платежей.

- **POST** `/api/payments/`
  - Создание нового платежа.

- **GET** `/api/payments/{id}/stripe/`
  - Получение статуса платежа
  
- **POST** `/api/payments/stripe`
  - Создание нового платежа в платежной системе stripe.
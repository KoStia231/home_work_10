# начало знакомства с api 

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

### Загрузка фикстуры с оплатой
```python
python manage.py loaddata pay.json  
```

---

## Пользователи в базе

> username-> ***admin@example.com***
>
>password-> ***admin***

> username-> ***kosta123139@gmail.com***
>
>password-> ***Hh14767Hh***
---

# API 
> http://localhost:8000/api/lessons   ***Список уроков***
> 
> http://localhost:8000/api/lessons/pk  ***Конкретный урок***
> 
> http://localhost:8000/api/courses/  ***Курсы***
> 
> http://localhost:8000/api/courses/pk  ***Конкретный курс***
> 
> http://localhost:8000/api/payments/ ***Оплата***
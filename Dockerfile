FROM python:3.12-slim

# Зависимости
RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /app

COPY . /app/

# Зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# копипаст скрипта в контейнер
COPY entrypoint.sh /entrypoint.sh

# Права выполнения скрипта
RUN chmod +x /entrypoint.sh

# Точка входа контейнера
ENTRYPOINT ["/entrypoint.sh"]
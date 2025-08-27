FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DOCKER_CONTAINER True

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles

# Copiar el script de espera
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

EXPOSE 8006

CMD ["/wait-for-db.sh", "db", "python", "manage.py", "collectstatic", "--noinput", "&&", "python", "manage.py", "migrate", "&&", "gunicorn", "--bind", "0.0.0.0:8006", "alkosto_verify.wsgi:application"]
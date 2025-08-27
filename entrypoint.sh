#!/bin/bash
# entrypoint.sh

set -e

# Función para esperar a que MySQL esté listo
wait_for_mysql() {
    echo "Waiting for MySQL at db:3306..."
    
    # Usar un método más confiable para verificar MySQL
    until python -c "
import pymysql
import time
import os
try:
    conn = pymysql.connect(
        host='db',
        user=os.environ.get('MYSQL_USER', 'alkosto_user'),
        password=os.environ.get('MYSQL_PASSWORD', 'alkosto_password'),
        database=os.environ.get('MYSQL_DATABASE', 'alkosto_verify_db'),
        port=3306
    )
    conn.close()
    print('MySQL is ready!')
except Exception as e:
    print(f'MySQL not ready: {e}')
    exit(1)
"; do
        echo "MySQL is unavailable - sleeping for 3 seconds"
        sleep 3
    done
}

# Esperar a que MySQL esté disponible
wait_for_mysql

echo "MySQL is up - proceeding with application startup"

# Crear directorios necesarios
mkdir -p /app/staticfiles

# Colectar archivos estáticos
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Aplicar migraciones
echo "Applying database migrations..."
python manage.py migrate

# Crear superusuario (opcional)
# python manage.py shell -c "
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(username='admin').exists():
#     User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
# "

echo "Starting application..."
# Ejecutar el comando principal (Gunicorn)
exec "$@"
#!/bin/sh

set -e

echo "Waiting for RabbitMQ to be ready..."
until nc -z rabbitmq 5672; do
    sleep 1
done
echo "RabbitMQ is ready"


echo "Waiting for PostgreSQL to start..."
python << END
import socket
import time
import os

host = "frontcore_db"
port = 5432

while True:
    try:
        with socket.create_connection((host, port), timeout=1):
            break
    except socket.error:
        print("PostgreSQL is unavailable - sleeping")
        time.sleep(1)

print("PostgreSQL started")
END

echo "Running migrations..."
python manage.py migrate
echo "Migrations complete"

echo "Starting consumer..."
python manage.py run_consumer

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
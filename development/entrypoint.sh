#!/bin/sh

echo "Starting entrypoint script..."

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      echo "PostgreSQL is unavailable - sleeping"
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Flushing Django database..."
python manage.py flush --no-input

echo "Running Django migrations..."
python manage.py migrate

echo "Starting Django server..."
exec "$@"

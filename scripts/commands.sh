#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

cron &

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py collectstatic --noinput

python manage.py makemigrations users --noinput
python manage.py migrate users --noinput

python manage.py makemigrations triage --noinput
python manage.py migrate triage --noinput

python manage.py makemigrations --noinput
python manage.py migrate --noinput

su -s /bin/sh -c 'python manage.py runserver 0.0.0.0:8000' duser

#!/usr/bin/env bash

# Wait until Postgres is ready
while ! pg_isready -q -h $PGHOST -p $PGPORT -U $PGUSER
do
  echo "$(date) - waiting for database to start"
  sleep 2
done

# Create, migrate, and seed database if it doesn't exist.
if [[ -z `psql -Atqc "\\list $PGDATABASE"` ]]; then
  echo "Database $PGDATABASE does not exist. Creating..."
  createdb -E UTF8 $PGDATABASE -l en_US.UTF-8 -T template0
  echo "Database $PGDATABASE created."
fi

# Running database updates
echo make migrations
python manage.py makemigrations
python manage.py migrate

mkdir staticfiles
python manage.py collectstatic --noinput

python manage.py test --noinput

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn callsAPI.wsgi:application --reload --bind 0.0.0.0:8000 --workers 3
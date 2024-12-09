#!/bin/sh

# Wait for database to be ready
if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL to be ready..."
  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 1
  done
  echo "PostgreSQL is ready."
fi

echo "Making database migrations..."
python manage.py makemigrations

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Loading parcel fixtures..."
{
  python manage.py loaddata api/parcel/fixtures/parcel_data.json
} || {
  echo "No data to load or an error occurred."
}

echo "Creating test user..."
{
  echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user('testuser', 'testpassword')" | python manage.py shell
} || {
  echo "Test user already exists."
}

echo "Running server..."
python manage.py runserver 0.0.0.0:8000

# Execute the CMD passed in the Dockerfile
exec "$@"
}
#!/bin/sh
set -e

# Run database migrations on container start
python manage.py migrate --noinput

# Start Gunicorn with increased timeout for long-running training requests
exec gunicorn portfolio.wsgi:application --bind 0.0.0.0:${PORT:-8000} --timeout 600

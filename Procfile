web: cd backend && gunicorn dealaai.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120 --access-logfile - --error-logfile -
worker: cd backend && celery -A dealaai worker --loglevel=info --concurrency=2
beat: cd backend && celery -A dealaai beat --loglevel=info

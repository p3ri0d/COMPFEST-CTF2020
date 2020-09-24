python3 manage.py makemigrations
python3 manage.py migrate
python manage.py loaddata seed
gunicorn pemulator.wsgi:application --bind 0.0.0.0:8000 --workers=8
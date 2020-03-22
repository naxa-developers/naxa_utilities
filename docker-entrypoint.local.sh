#pip install -r requirements.txt
python manage.py collectstatic --no-input
# python manage.py compilemessages -l ne -l en
python manage.py migrate --no-input
#pytest
#django-admin startproject naxa_utilities
python manage.py runserver 0.0.0.0:8000

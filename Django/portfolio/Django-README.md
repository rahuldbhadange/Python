pip install Django==2.2
mkdir project
python -m venv django-venv
    cd django-venv
        script\activate 
  
django-admin startproject your-project-name
 
 
 __init__.py => package 
 settings.py => project setiings
 urls.py => project urls
 wsgi.py => web server gateway
 
 manage.py => will be used during project
 
 cd your-app-name
    python manage.py runserver
    - http://127.0.0.0:8080/
    python manage.py startapp your_app_name
    __init__ =>
    admin=> to register models, Django will then use them with Django's admin
    app.py => app specific config
    models.py => applications data and relationship of data
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py createapp your_app_name
        models.py => allows user to store data in the database in a specific way.
 
 
 
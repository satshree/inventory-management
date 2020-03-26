## About ##

A Very Basic Inventory Management System made for Mercantile Communications, Nepal.  

## Requirements ##

1. Python 3.*  
2. pip3 and pipenv

## How do I get set up? ##

This app is made with Django. Follow these steps to run this app,  

1. Run 'pipenv update' to install the dependencies in a virtual environment.  
2. Run 'pipenv shell' to activate virtual environment.    
3. Change directory to 'inventory'. (command: 'cd inventory')  
4. Run 'python manage.py migrate' to migrate database. (Only for first time when setting up the app.)  
5. Run 'python manage.py createsuperuser' to create a super user. (If there is no super user.)  
6. Run 'python manage.py create-groups' to create user privileges. (Only for first time when setting up the app.)  
7. Run 'python manage.py runserver' to run the app.  

#### DEBUG is set to 'False'. Create 'local_settings.py' where 'settings.py' is. Copy everything from 'sample_local_settings.py' and override DEBUG = True if needed. #### 

## Authors ##

Aashirwad Shrestha  
Satshree Shrestha  
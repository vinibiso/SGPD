# SGPD

**A Distributed processing system for breaking MD5 Hashes, made using Django to break the problem and Javascrit to process the pieces**

## Setup:
**Clone this repository**

Change the DATABASES array in sgpd > settings.py

### It could look something like:
```py
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'spgd',
          'USER': 'root',
          'PASSWORD': '',
          'HOST': '127.0.0.1',
          'PORT': '3306',
      }
  }
```
### And then do:
```shell
  python manage.py syncdb
  python manage.py runserver  
```

**Don't forget to make sure your mysql server is runing, you could also use SQLite**

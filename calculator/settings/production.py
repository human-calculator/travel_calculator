from calculator.settings.base import *

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "travel_calculator",
        'USER': os.environ.get("DATABASE_USER"),
        'PASSWORD': os.environ.get("DATABASE_PW"),
        'HOST': os.environ.get("DATABASE_HOST"),
        'PORT': 3306,
    }
}

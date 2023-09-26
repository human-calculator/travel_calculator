import os
import sys

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/travel_calculator")
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "calculator.settings.base")
load_dotenv(
    os.path.join(BASE_DIR, '.env')
)

import django
django.setup()

from currencies.services import CurrencyScheduleManager

if __name__ == '__main__':
    CurrencyScheduleManager().execute()

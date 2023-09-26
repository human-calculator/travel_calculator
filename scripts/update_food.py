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

from food.models import FoodPrice


if __name__ == '__main__':
    data = {
        "LAX": 20797,
        "JFK": 32496,
        "YVR": 25211,
        "SFO": 25997,
        "YYZ": 20169,
        "LAS": 22097,
        "ORD": 23397,
        "SEA": 24697,
        "IAD": 22097,
        "GUM": 32496,
        "SYD": 17925,
        "AKL": 20217,
        "BNE": 17925,
        "MEL": 17925,
        "HKT": 4049,
        "KUL": 4425,
        "MFM": 8849,
        "BKI": 3540,
        "SIN": 11210,
        "HAN": 2791,
        "HKG": 9939,
        "SGN": 2791,
        "DAD": 2233,
        "BKK": 2576,
        "NGO": 7617,
        "CTS": 9997,
        "OKA": 8569,
        "FUK": 9521,
        "HND": 9521,
        "KIX": 9521,
        "CAI": 5531,
        "DXB": 12386,
        "HVN": 12998,
        "BOG": 4730,
        "SCL": 10518,
        "EZE": 9008,
        "MEX": 9678,
        "LIM": 4935,
        "ZAG": 11731,
        "AMS": 24458,
        "ZHR": 34054,
        "VCE": 20382,
        "VIE": 20382,
        "MAD": 16985,
        "MUC": 20382,
        "IST": 5475,
        "PRG": 9887,
        "FCO": 24833,
        "FRA": 16305,
        "BCN": 17596,
        "LHR": 31537,
        "CDG": 20382
    }

    print("[START]")

    for city in data:
        print(f'city : {city} / price : {data[city]}')
        FoodPrice.objects.create(city_code=city, amount=data[city])

    print("[END]")

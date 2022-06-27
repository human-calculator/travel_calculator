import os
import sys

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/travel_calculator")
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "calculator.settings")
load_dotenv(
    os.path.join(BASE_DIR, '.env')
)

import django
django.setup()

from flight.services.flight import FlightScheduleManager
from hotels.services.schedule_manager import HotelScheduleManager

if __name__ == '__main__':
    city_code_list = [
        "LAX",
        "JFK",
        "YVR",
        "SFO",
        "YYZ",
        "LAS",
        "ORD",
        "SEA",
        "IAD",
        "GUM",
        "SYD",
        "SPN",
        "AKL",
        "BNE",
        "MEL",
        "GRU",
        "GIG",
        "LIM",
        "MEX",
        "CUN",
        "EZE",
        "SCL",
        "BOG",
        "HAV",
        "KTM",
        "DEL",
        "BOM",
        "BLR",
        "CCU",
        "ULN",
        "DXB",
        "IKA",
        "DOH",
        "CAI",
        "KIX",
        "NRT",
        "HND",
        "FUK",
        "OKA",
        "CTS",
        "NGO",
        "PVG",
        "CAN",
        "PEK",
        "TAO",
        "SHA",
        "BKK",
        "DAD",
        "SGN",
        "HKG",
        "TPE",
        "MNL",
        "HAN",
        "SIN",
        "CEB",
        "BKI",
        "MFM",
        "CXR",
        "KUL",
        "HKT"
    ]

    flight_fail_list = []
    flight_success_list = []
    hotel_fail_list = []
    hotel_success_list = []
    success_list = []
    for city_code in city_code_list:
        try:
            print(f'{city_code} - flight checking!')
            FlightScheduleManager().execute_by_city_code(city_code)
            flight_success_list.append(city_code)
        except Exception:
            flight_fail_list.append(city_code)

        try:
            print(f'{city_code} - hotel checking!')
            HotelScheduleManager().execute_by_city_code(city_code)
            hotel_success_list.append(city_code)
        except Exception:
            hotel_fail_list.append(city_code)

        if city_code in flight_success_list and city_code in hotel_success_list:
            success_list.append(city_code)

    print('flight_fail_list :', flight_fail_list)
    print('=====================================')

    print('flight_success_list :', flight_success_list)
    print('=====================================')

    print('hotel_fail_list :', hotel_fail_list)
    print('=====================================')

    print('hotel_success_list :', hotel_success_list)
    print('=====================================')

    print('success_list :', success_list)
    print('=====================================')

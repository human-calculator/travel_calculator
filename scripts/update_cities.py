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

CITY_INFOS = [
    ("CDG", "파리", "Paris", "프랑스", "France"),
    ("LHR", "런던", "London", "영국", "United Kingdom"),
    ("BCN", "바르셀로나", "Barcelona", "스페인", "Spain"),
    ("FRA", "프랑크푸르트", "Frankfurt", "독일", "Germany"),
    ("FCO", "로마", "Rome", "이탈리아", "Italy"),
    ("PRG", "프라하", "Prague", "체코", "Czech Republic"),
    ("IST", "이스탄불", "Istanbul", "터키", "Turkey"),
    ("MUC", "뮌헨", "Munich", "독일", "Germany"),
    ("MAD", "마드리드", "Madrid", "스페인", "Spain"),
    ("VIE", "비엔나", "Vienna", "오스트리아", "Austria"),
    ("VCE", "베니스", "Venice", "이탈리아", "Italy"),
    ("ZRH", "취리히", "Zurich", "스위스", "Switzerland"),
    ("AMS", "암스테르담", "Amsterdam", "네덜란드", "Netherlands"),
    ("ZAG", "자그레브", "Zagreb", "크로아티아", "Croatia"),
    ("LAX", "로스앤젤레스", "Los Angeles", "미국", "United States"),
    ("JFK", "뉴욕", "New York", "미국", "United States"),
    ("SFO", "샌프란시스코", "San Francisco", "미국", "United States"),
    ("LAS", "라스베이거스", "Las Vegas", "미국", "United States"),
    ("ORD", "시카고", "Chicago", "미국", "United States"),
    ("SEA", "시애틀", "Seattle", "미국", "United States"),
    ("IAD", "워싱턴", "Washington", "미국", "United States"),
    ("YVR", "밴쿠버", "Vancouver", "캐나다", "Canada"),
    ("YYZ", "토론토", "Toronto", "캐나다", "Canada"),
    ("SYD", "시드니", "Sydney", "호주", "Australia"),
    ("GUM", "괌", "Guam", "미국", "United States"),
    ("AKL", "오클랜드", "Auckland", "뉴질랜드", "New Zealand"),
    ("BNE", "브리즈번", "Brisbane", "호주", "Australia"),
    ("MEL", "멜버른", "Melbourne", "호주", "Australia"),
    ("LIM", "리마", "Lima", "페루", "Peru"),
    ("MEX", "멕시코 시티", "Mexico City", "멕시코", "Mexico"),
    ("EZE", "부에노스 아이레스", "Buenos Aires", "아르헨티나", "Argentina"),
    ("SCL", "산티아고", "Santiago", "칠레", "Chile"),
    ("BOG", "보고타", "Bogota", "콜롬비아", "Colombia"),
    ("HAV", "하바나", "Havana", "쿠바", "Cuba"),
    ("DXB", "두바이", "Dubai", "아랍에미리트", "United Arab Emirates"),
    ("CAI", "카이로", "Cairo", "이집트", "Egypt"),
    ("KIX", "오사카", "Osaka", "일본", "Japan"),
    ("NRT", "도쿄", "Tokyo", "일본", "Japan"),
    ("HND", "도쿄", "Tokyo", "일본", "Japan"),
    ("FUK", "후쿠오카", "Fukuoka", "일본", "Japan"),
    ("OKA", "오키나와", "Okinawa", "일본", "Japan"),
    ("CTS", "삿포로", "Sapporo", "일본", "Japan"),
    ("NGO", "나고야", "Nagoya", "일본", "Japan"),
    ("BKK", "방콕", "Bangkok", "태국", "Thailand"),
    ("DAD", "다낭", "Da Nang", "베트남", "Vietnam"),
    ("SGN", "호치민시", "Ho Chi Minh City", "베트남", "Vietnam"),
    ("HKG", "홍콩", "Hong Kong", "홍콩", "Hong Kong"),
    ("HAN", "하노이", "Hanoi", "베트남", "Vietnam"),
    ("SIN", "싱가포르", "Singapore", "싱가포르", "Singapore"),
    ("BKI", "코타키나발루", "Kota Kinabalu", "말레이시아", "Malaysia"),
    ("MFM", "마카오", "Macau", "마카오", "Macau"),
    ("KUL", "쿠알라룸푸르", "Kuala Lumpur", "말레이시아", "Malaysia"),
    ("HKT", "푸켓", "Phuket", "태국", "Thailand"),
]


def update_cities():
    """
    도시 City 및 국가 Country 정보 생성 스크립트
    """
    from cities.models import Country, City

    for airport_code, city_kor, city_eng, country_kor, country_eng in CITY_INFOS:
        country, created = Country.objects.get_or_create(
            eng_name=country_eng, kor_name=country_kor
        )

        City.objects.create(
            city_code=airport_code,
            eng_name=city_eng,
            kor_name=city_kor,
            country_id=country
        )


if __name__ == '__main__':
    update_cities()

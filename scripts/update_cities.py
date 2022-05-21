#!/usr/bin/env python
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calculator.settings')

import django
django.setup()

from cities.models import Country, City


def update_cities():
	Country.objects.all().delete()
	City.objects.all().delete()
	
	france = Country.objects.create(
		eng_name="France",
		kor_name="프랑스"
	)
	
	City.objects.create(
		city_code="PAR",
		eng_name="Paris",
		kor_name="파리",
		country_id=france
	)
	
	england = Country.objects.create(
		eng_name="The United Kingdom of Great Britain and Northern Ireland",
		kor_name="영국"
	)
	
	City.objects.create(
		city_code="LHR",
		eng_name="London",
		kor_name="런던",
		country_id=england
	)
	
	japan = Country.objects.create(
		eng_name="Japan",
		kor_name="일본"
	)
	
	City.objects.create(
		city_code="NRT",
		eng_name="Tokyo",
		kor_name="도쿄",
		country_id=japan
	)

	portugal = Country.objects.create(
		eng_name="Portuguese Republic",
		kor_name="일본"
	)
	
	City.objects.create(
		city_code="LIS",
		eng_name="Lisbon",
		kor_name="리스본",
		country_id=portugal
	)


if __name__ == '__main__':
	update_cities()

import os
from datetime import date, timedelta, datetime
from statistics import mean, median
from typing import Optional

from django.db.models import Sum

from amadeus import Client

from cities.models import City
from hotels.models import HotelPrice, ParsedHotelPriceData
from currencies.models import Currency
from collections import defaultdict


class HotelPriceService:
	
	def __init__(self, city_code: str):
		self._city_code = city_code
		
	def get_hotel_price_by_period(self, from_date, to_date):
		return HotelPrice.objects.filter(
			city_code=self._city_code,
			check_in_date__gte=from_date,
			check_in_date__lte=to_date
		).aggregate(Sum('median_price')).get("median_price__sum")
	

class AmadeusCommander:
	CLIENT_ID = os.environ.get("CLIENT_ID")
	CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

	def _get_price_currency(self, price_data):
		try:
			return price_data[0].get("offers")[0].get("price").get("currency")
		except:
			raise Exception

	def _parse_price_data(self, price_data):
		date_price_dict = defaultdict(list)
		for offer in price_data:
			detail_offers = offer.get("offers")
			for detail_offer in detail_offers:
				price_dict = detail_offer.get("price")
				changes = price_dict.get("variations").get("changes")
				for change in changes:
					start_date_str = change.get("startDate")
					end_date_str = change.get("endDate")
					start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
					end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
					
					target_date = start_date
					while start_date <= target_date < end_date:
						period_price = float(change.get("total") if change.get("total") else change.get("base"))
						date_price_dict[target_date.strftime("%Y-%m-%d")].append(period_price)
						target_date = target_date + timedelta(days=1)
		
		print("date_price_dict :", date_price_dict)
		return date_price_dict

	def get_hotel_price_from_amadeus(
		self,
		city_code: str,
		check_in_date: date,
		check_out_date: Optional[date] = None
	) -> ParsedHotelPriceData:
		if check_out_date is None:
			check_out_date = check_in_date + timedelta(days=99)

		amadeus = Client(
			client_id=self.CLIENT_ID,
			client_secret=self.CLIENT_SECRET
		)
		params = {
			"cityCode": city_code,
			"roomQuantity": 1,
			"adults": 1,
			"radius": 30,
			"radiusUnit": "KM",
			"paymentPolicy": None,
			"includeClosed": False,
			"bestRateOnly": True,
			"view": "FULL",
			"checkInDate": check_in_date.strftime("%Y-%m-%d"),
			"checkOutDate": check_out_date.strftime("%Y-%m-%d"),
			"ratings": "3",
			"currency": "USD"
		}
		response = amadeus.shopping.hotel_offers.get(**params)
		return ParsedHotelPriceData(
			price_list=self._parse_price_data(response.data),
			cur_unit=self._get_price_currency(response.data)
		)
		

class HotelScheduleManager:
	_amadeus_commander = AmadeusCommander()
		
	def _update_hotel_price(
		self,
		city_code: str,
		check_in_date: date
	):
		parsed_hotel_price_data = self._amadeus_commander.get_hotel_price_from_amadeus(city_code, check_in_date)
		cur_unit = parsed_hotel_price_data.cur_unit
		for target_date, price_list in parsed_hotel_price_data.price_list.items():
			# TODO 가격 검증해서 수정 필요함
			price_list = list(set(price_list))
			max_price = max(price_list)
			min_price = min(price_list)
			avg_price = mean(price_list)
			median_price = median(price_list)

			print(f"[UPDATE HOTEL PRICE] city_code : {city_code}, target_date : {target_date}, max : {max_price}, min : {min_price}, avg : {avg_price}, median : {median_price}")
			
			HotelPrice.objects.create(
				city_code=city_code,
				check_in_date=target_date,
				min_price=self._convert_currency(min_price, cur_unit),
				max_price=self._convert_currency(max_price, cur_unit),
				median_price=self._convert_currency(median_price, cur_unit)
			)

	@staticmethod
	def _convert_currency(
		price: float,
		cur_unit: str
	):
		currency = Currency.objects.filter(cur_unit=cur_unit).first()
		if currency:
			return price * currency.ttb
		else:
			raise Exception

	def execute(self):
		cities = City.objects.all()
		target_date = datetime.today()
		for city in cities:
			self._update_hotel_price(city.city_code, target_date)

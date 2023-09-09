import traceback
from datetime import date, datetime
from statistics import mean, median

from calculator.utils import send_slack
from cities.models import City
from hotels.models import HotelPrice
from hotels.services.amadeus_hotel_commander import AmadeusHotelCommander
from utils import convert_currency


class HotelScheduleManager:
	_amadeus_commander = AmadeusHotelCommander()

	def _update_hotel_price(
		self,
		city_code: str,
		check_in_date: date
	):
		parsed_hotel_price_data = self._amadeus_commander.get_hotel_price_from_amadeus(city_code, check_in_date)
		cur_unit = parsed_hotel_price_data.cur_unit
		print("cur_unit ::", cur_unit)
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
				min_price=convert_currency(min_price, cur_unit),
				max_price=convert_currency(max_price, cur_unit),
				median_price=convert_currency(median_price, cur_unit)
			)

	def execute(self):
		try:
			cities = City.objects.all()
			target_date = datetime.today()
			for city in cities:
				self._update_hotel_price(city.city_code, target_date)

		except Exception as e:
			err_msg = traceback.format_exc()
			send_slack(f":ghost: [FAILED] [SCHEDULE] [HOTEL] {err_msg}")

	def execute_by_city_code(
		self,
		city_code: str
	):
		target_date = datetime.today()
		self._update_hotel_price(city_code, target_date)

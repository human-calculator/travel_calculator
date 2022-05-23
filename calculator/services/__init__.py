from datetime import date
from urllib.request import urlopen

from calculator.models import TravelExpenses
from calculator.services.food import FoodExpenseCalculator
from calculator.services.hotel import HotelExpenseCalculator
from flight.services.flight import FlightCalculateService

import ssl

ONE_MEAL_PRICE = 10000


class Calculator:
	def __init__(self, city_code: str, from_date: date, to_date: date):
		self._city_code = city_code
		self._from_date = from_date
		self._to_date = to_date

		self._nights = (to_date - from_date).days
		self._days = self._nights + 1

	def calculate(self) -> TravelExpenses:
		flight_expense = int(FlightCalculateService().calculate(
			departure_date=self._from_date.strftime("%Y-%m-%d"),
			arrival_date=self._to_date.strftime("%Y-%m-%d"),
			destination=self._city_code
		))
		hotel_expense = int(HotelExpenseCalculator(self._city_code).get_hotel_price_by_period(
			from_date=self._from_date,
			to_date=self._to_date,
		))

		meal_expense = int(
			FoodExpenseCalculator(self._city_code).get_food_price(ONE_MEAL_PRICE) * 3 * self._nights
		)

		return TravelExpenses(
			flight_expense=flight_expense,
			hotel_expense=hotel_expense,
			meal_expense=meal_expense,
			total_expense=flight_expense + hotel_expense + meal_expense,
			from_date=self._from_date,
			to_date=self._to_date,
			nights=self._nights,
			days=self._days,
			destination=self._city_code
		)


def ssl_disabled_urlopen(endpoint):
	return urlopen(endpoint, context=ssl._create_unverified_context())

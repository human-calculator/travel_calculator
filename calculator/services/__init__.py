from datetime import date

from calculator.models import TravelExpenses
from food.services.calculator import FoodExpenseCalculator
from flight.services.flight import FlightCalculateService
from hotels.services.calculator import HotelExpenseCalculator

ONE_MEAL_PRICE = 10000


class Calculator:
	def __init__(self, city_code: str, from_date: date, to_date: date):
		self._city_code = city_code
		self._from_date = from_date
		self._to_date = to_date

		self._nights = (to_date - from_date).days
		self._days = self._nights + 1

	def calculate(self) -> TravelExpenses:
		flight_expense = FlightCalculateService().calculate(
			departure_date=self._from_date.strftime("%Y-%m-%d"),
			arrival_date=self._to_date.strftime("%Y-%m-%d"),
			destination=self._city_code
		)
		hotel_expense = HotelExpenseCalculator(self._city_code).get_hotel_price_by_period(
			from_date=self._from_date,
			to_date=self._to_date,
		)

		meal_expense = FoodExpenseCalculator(self._city_code).get_food_price(ONE_MEAL_PRICE) * 3 * self._nights

		return TravelExpenses(
			flight_expense=int(flight_expense) if flight_expense else None,
			hotel_expense=int(hotel_expense) if hotel_expense else None,
			meal_expense=int(meal_expense) if meal_expense else None,
			total_expense=flight_expense + hotel_expense + meal_expense,
			from_date=self._from_date,
			to_date=self._to_date,
			nights=self._nights,
			days=self._days,
			destination=self._city_code
		)

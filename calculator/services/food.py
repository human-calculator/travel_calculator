from food.models import FoodPrice


class FoodPriceService:

	def __init__(self, city_code: str):
		self._city_code = city_code

	def _get_food_price_ratio(self):
		food_price = FoodPrice.objects.filter(
			city_code=self._city_code
		).first()
		return food_price.amount_to_korea_amount_ratio

	def get_food_price(self, amount: int):
		return round(self._get_food_price_ratio() * amount, 0)

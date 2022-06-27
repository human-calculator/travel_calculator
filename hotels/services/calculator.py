from django.db.models import Sum

from hotels.models import HotelPrice


class HotelExpenseCalculator:

	def __init__(self, city_code: str):
		self._city_code = city_code

	def get_hotel_price_by_period(self, from_date, to_date):
		return HotelPrice.objects.filter(
			city_code=self._city_code,
			check_in_date__gte=from_date,
			check_in_date__lte=to_date
		).aggregate(Sum('median_price')).get("median_price__sum")
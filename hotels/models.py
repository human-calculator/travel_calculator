from dataclasses import dataclass
from typing import List, Dict

from django.db import models


class HotelPrice(models.Model):
	city_code = models.CharField(max_length=20)
	check_in_date = models.DateField()
	min_price = models.FloatField()
	max_price = models.FloatField()
	median_price = models.FloatField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


@dataclass
class ParsedHotelPriceData:
	price_list: Dict[str, List[float]]
	cur_unit: str

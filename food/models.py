from django.db import models

# Create your models here.


SOUTH_KOREA_FOOD_PRICE = 1089897.13


class FoodPrice(models.Model):
	city_code = models.CharField(max_length=32)
	amount = models.FloatField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	@property
	def amount_to_korea_amount_ratio(self):
		return self.amount / SOUTH_KOREA_FOOD_PRICE

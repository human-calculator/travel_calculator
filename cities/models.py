from django.db import models


class Country(models.Model):
	eng_name = models.CharField(max_length=128)
	kor_name = models.CharField(max_length=128)


class City(models.Model):
	city_code = models.CharField(max_length=32)
	eng_name = models.CharField(max_length=64)
	kor_name = models.CharField(max_length=32)
	country_id = models.ForeignKey("Country", related_name="country", on_delete=models.CASCADE, db_column="country_id")

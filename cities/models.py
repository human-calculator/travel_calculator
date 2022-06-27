from django.db import models


class Country(models.Model):
	eng_name = models.CharField(max_length=128, verbose_name="영문명")
	kor_name = models.CharField(max_length=128, verbose_name="한글명")


class City(models.Model):
	city_code = models.CharField(max_length=32, verbose_name="도시코드")
	eng_name = models.CharField(max_length=64, verbose_name="영문명")
	kor_name = models.CharField(max_length=32, verbose_name="한글명")
	country_id = models.ForeignKey(
		"Country", related_name="country", on_delete=models.CASCADE, db_column="country_id"
	)

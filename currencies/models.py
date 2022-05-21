from django.db import models


class Currency(models.Model):
	cur_unit = models.CharField(max_length=32, verbose_name="통화코드")
	cur_nm = models.CharField(max_length=64, verbose_name="국가/통화명")
	ttb = models.FloatField(max_length=64, verbose_name="살 때")  # 환율 계산시 이용
	tts = models.FloatField(max_length=64, verbose_name="팔 때")
	deal_bas_r = models.FloatField(max_length=64, verbose_name="매매 기준율")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

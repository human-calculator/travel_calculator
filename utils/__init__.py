import ssl
from urllib.request import urlopen

from currencies.models import Currency


def convert_currency(
	price: float,
	cur_unit: str
):
	currency = Currency.objects.filter(cur_unit=cur_unit).first()
	if currency:
		return price * currency.ttb
	else:
		raise Exception("no currency info")


def ssl_disabled_urlopen(endpoint):
	return urlopen(endpoint, context=ssl._create_unverified_context())
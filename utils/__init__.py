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

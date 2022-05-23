import os
from collections import defaultdict
from datetime import datetime, timedelta, date
from typing import Optional

from amadeus import Client

from hotels.models import ParsedHotelPriceData


class AmadeusHotelCommander:
	AMADEUS_CLIENT_ID = os.environ.get("AMADEUS_CLIENT_ID")
	AMADEUS_CLIENT_SECRET = os.environ.get("AMADEUS_CLIENT_SECRET")

	def __init__(self):
		self._amadeus_client = Client(
			client_id=self.AMADEUS_CLIENT_ID,
			client_secret=self.AMADEUS_CLIENT_SECRET
		)

	def _get_price_currency(self, price_data):
		try:
			return price_data[0].get("offers")[0].get("price").get("currency")
		except:
			raise Exception("no currency info")

	def _parse_price_data(self, price_data):
		date_price_dict = defaultdict(list)
		for offer in price_data:
			detail_offers = offer.get("offers")
			for detail_offer in detail_offers:
				price_dict = detail_offer.get("price")
				changes = price_dict.get("variations").get("changes")
				for change in changes:
					start_date_str = change.get("startDate")
					end_date_str = change.get("endDate")
					start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
					end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

					target_date = start_date
					while start_date <= target_date < end_date:
						period_price = float(change.get("total") if change.get("total") else change.get("base"))
						date_price_dict[target_date.strftime("%Y-%m-%d")].append(period_price)
						target_date = target_date + timedelta(days=1)

		print("date_price_dict :", date_price_dict)
		return date_price_dict

	def get_hotel_price_from_amadeus(
		self,
		city_code: str,
		check_in_date: date,
		check_out_date: Optional[date] = None
	) -> ParsedHotelPriceData:
		if check_out_date is None:
			check_out_date = check_in_date + timedelta(days=99)

		params = {
			"cityCode": city_code,
			"roomQuantity": 1,
			"adults": 1,
			"radius": 30,
			"radiusUnit": "KM",
			"paymentPolicy": None,
			"includeClosed": False,
			"bestRateOnly": True,
			"view": "FULL",
			"checkInDate": check_in_date.strftime("%Y-%m-%d"),
			"checkOutDate": check_out_date.strftime("%Y-%m-%d"),
			"ratings": "3",
			"currency": "USD"
		}
		response = self._amadeus_client.shopping.hotel_offers.get(**params)
		return ParsedHotelPriceData(
			price_list=self._parse_price_data(response.data),
			cur_unit=self._get_price_currency(response.data)
		)

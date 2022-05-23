import datetime
import math
import os
from typing import List, Dict, Any
from amadeus import Client

from calculator.services import ssl_disabled_urlopen
from cities.models import City
from currencies.models import Currency
from flight.models.flight import FlightOffer, Cabin, FlightSummary, FlightSearchPayload, FlightPrice


class FlightCalculateService:
    base_location = "ICN"

    def calculate(self, departure_date: str, arrival_date: str, destination: str) -> float:
        departure = FlightSummary.objects.filter(
            departure_date=departure_date,
            origin=self.base_location,
            destination=destination
        ).first()

        arrive = FlightSummary.objects.filter(
            departure_date=arrival_date,
            origin=destination,
            destination=self.base_location
        ).first()

        return (departure.price + arrive.price) * 0.8


class FlightSummarizeService:
    """
    날짜별 항공정보를 조회하여 평균 값을 연산하고 연산 결과를 저장합니다.
    """
    api_counter = 0  # API 호출 횟수
    api_limit = 2000  # API 호출 제한

    max_stop = 1  # 최대 경유
    base_location = "ICN"
    default_cabin = Cabin.ECONOMY

    amadeus: Client
    exchange_rate: Dict

    def __init__(self, destinations: List):
        client_id = os.environ.get("AMADEUS_CLIENT_ID")
        client_secret = os.environ.get("AMADEUS_CLIENT_SECRET")
        self.amadeus = Client(client_id=client_id, client_secret=client_secret, http=ssl_disabled_urlopen)
        self.destinations = destinations

    def summarize(self, target_dates: List[str]):
        latest_date = ""

        self._set_exchange_rate()

        for target_date in target_dates:
            self.api_counter += len(self.destinations) * 2
            if self.api_counter >= self.api_limit:
                print(f"{datetime.datetime.now()} [FLIGHT] [SUMMARIZE] {latest_date} 까지의 항공 정보가 업데이트 되었습니다.")
                break

            self._summarize_offers_by_date(target_date=target_date)
            latest_date = target_date

    def _set_exchange_rate(self):
        currencies = Currency.objects.all()
        exchange_rate = dict()
        for currency in currencies:
            exchange_rate[currency.cur_unit] = currency.ttb
        self.exchange_rate = exchange_rate

    def _get_exchange_rate(self, currency: str) -> float:
        rate = self.exchange_rate.get(currency)
        if not rate:
            print(f"[FLIGHT] [CURRENCY] 해당 통화의 환율 정보가 존재하지 않습니다. {currency}")
            raise Exception(f"[FLIGHT] [CURRENCY] 해당 통화의 환율 정보가 존재하지 않습니다. {currency}")

        return rate

    def _exchange_for_krw(self, currency: str, total: float, base: float) -> FlightPrice:
        rate = self._get_exchange_rate(currency=currency)
        return FlightPrice(
            currency="KRW",
            total=round(total * rate),
            base=round(base * rate)
        )

    def _sanitize_result(self, payload: FlightSearchPayload, result: List[Dict]) -> List[FlightOffer]:
        offers = []

        if not result:
            return offers

        for data in result:
            itineraries = data.get("itineraries")

            try:
                for itinerary in itineraries:
                    for segment in itinerary.get("segments"):
                        stop = segment.get("numberOfStops")
                        if stop and stop > self.max_stop:
                            raise Exception(f"[FLIGHT] [STOP] 경유 {stop} 이상은 포함하지 않습니다.")
            except Exception as e:
                continue

            price = data.get("price")
            if not price:
                continue

            currency = price.get("currency")
            total = price.get("total")
            base = price.get("base")
            if not currency or not total or not base:
                continue

            try:
                exchanged_price = self._exchange_for_krw(
                    currency=currency,
                    total=float(total),
                    base=float(base)
                )
            except Exception as e:
                continue

            offers.append(FlightOffer(
                origin=payload.origin,
                destination=payload.destination,
                departure_date=payload.departure_date,
                cabin=payload.cabin,
                price=exchanged_price
            ))

        return offers

    def _compute_summary(self, payload: FlightSearchPayload, offers: List[FlightOffer]) -> Dict[str, Any]:
        ten_percent = math.floor(len(offers) / 10)
        sorted_offers = sorted(offers, key=lambda x: x.price.total)

        if len(offers) > 100:
            min_truncated_offers = sorted_offers[ten_percent:len(offers)-ten_percent]
            truncated_offers = min_truncated_offers[:100]
        else:
            ten_percent = math.floor(len(offers) / 10)
            sorted_offers = sorted(offers, key=lambda x: x.price.total)
            truncated_offers = sorted_offers[ten_percent:len(offers) - ten_percent]

        sum_of_offers = sum(offer.price.total for offer in truncated_offers)
        average_of_offers = sum_of_offers / len(truncated_offers)

        return dict(
            origin=payload.origin,
            destination=payload.destination,
            departure_date=payload.departure_date,
            price=round(average_of_offers)
        )

    def _summarize_offers_by_date(self, target_date: str):
        for destination in self.destinations:
            depart_payload = FlightSearchPayload(
                origin=self.base_location,
                destination=destination,
                departure_date=target_date,
                cabin=self.default_cabin
            )

            arrive_payload = FlightSearchPayload(
                origin=destination,
                destination=self.base_location,
                departure_date=target_date,
                cabin=self.default_cabin
            )

            depart_result = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=depart_payload.origin,
                destinationLocationCode=depart_payload.destination,
                departureDate=target_date,
                adults='1',
                travelClass=Cabin.ECONOMY.value
            ).data

            arrive_result = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=arrive_payload.origin,
                destinationLocationCode=arrive_payload.destination,
                departureDate=target_date,
                adults='1',
                travelClass=Cabin.ECONOMY.value
            ).data

            depart_offers = self._sanitize_result(payload=depart_payload, result=depart_result)
            arrive_offers = self._sanitize_result(payload=arrive_payload, result=arrive_result)

            depart_summary = self._compute_summary(payload=depart_payload, offers=depart_offers)
            arrive_summary = self._compute_summary(payload=arrive_payload, offers=arrive_offers)

            print(depart_summary)
            print(arrive_summary)

            FlightSummary.objects.create(**depart_summary)
            FlightSummary.objects.create(**arrive_summary)


class FlightScheduleManager:
    limit_per_day = 30

    def get_latest_summarized_summary(self) -> FlightSummary:
        return FlightSummary.objects.all().order_by("-created_at")[0]

    def get_target_start_date(self) -> datetime.date:
        # 가장 마지막으로 업데이트 된 기록의 날짜가 조회 시점으로부터 약 12개월
        # - 후라면, 오늘을 포함하여 limit_per_day 만큼 조회
        # - 전이라면, 마지막 기록의 다음날을 포함하여 limit_per_day 만큼을 조회한다.

        today = datetime.date.today()
        latest_summarized_summary = self.get_latest_summarized_summary()

        if latest_summarized_summary and latest_summarized_summary.departure_date >= today + datetime.timedelta(weeks=48):
            return latest_summarized_summary.departure_date + datetime.timedelta(days=1)
        else:
            return today

    def get_target_dates(self) -> List[str]:
        targets = []

        start_date = self.get_target_start_date()
        for day in range(self.limit_per_day):
            targets.append((start_date + datetime.timedelta(days=day)).strftime('%Y-%m-%d'))

        return targets

    def execute(self):
        target_dates = self.get_target_dates()
        cities = City.objects.all()
        for city in cities:
            FlightSummarizeService(city.city_code).summarize(target_dates=target_dates)

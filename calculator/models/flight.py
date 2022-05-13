from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from django.db import models


class Cabin(Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"


@dataclass
class FlightSearchPayload:
    origin: str
    destination: str
    departure_date: str
    cabin: Cabin


@dataclass
class FlightPrice:
    total: float
    base: float
    currency: str = "KRW"


@dataclass
class FlightOffer:
    origin: str
    destination: str
    departure_date: str
    cabin: Cabin
    price: FlightPrice


class FlightSummary(models.Model):
    origin: str
    destination: str
    departure_date: str
    # departure_datetime: datetime
    price: float

    class Meta:
        ordering = ("-id",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

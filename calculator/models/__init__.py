from dataclasses import dataclass
from datetime import date


@dataclass
class TravelExpenses:
	flight_expense: int
	hotel_expense: int
	meal_expense: int
	total_expense: int
	from_date: date
	to_date: date
	nights: int
	days: int
	destination: str  # City?
	traveler_count: int = 1

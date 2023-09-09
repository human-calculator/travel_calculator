import traceback
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from calculator.services import Calculator
from calculator.utils import send_slack


# @csrf_exempt
def calculate(request):
	try:
		from_date = request.GET.get('from_date', None)
		to_date = request.GET.get('to_date', None)

		from_date = datetime.strptime(from_date, "%Y-%m-%d")
		to_date = datetime.strptime(to_date, "%Y-%m-%d")
		city_code = request.GET.get('city_code', None)

		travel_expenses = Calculator(city_code, from_date, to_date).calculate()
		send_slack(
			f":airplane: [SUCCESS] [API] *[{from_date} ~ {to_date} {city_code}]* \n항공권: {travel_expenses.flight_expense} 원\n숙박: {travel_expenses.hotel_expense} 원\n식비: {travel_expenses.meal_expense} 원\n총: {travel_expenses.total_expense} 원")
		return JsonResponse(travel_expenses.__dict__)

	except Exception as e:
		err_msg = traceback.format_exc()
		send_slack(f":ghost: [FAILED] [API] {err_msg}")
from datetime import datetime

from calculator.services import Calculator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def calculate(request):
	req_dict = request.POST.dict()
	from_date = datetime.strptime(req_dict.get("from_date"), "%Y-%m-%d")
	to_date = datetime.strptime(req_dict.get("to_date"), "%Y-%m-%d")
	city_code = req_dict.get("city_code")

	travel_expenses = Calculator(city_code, from_date, to_date).calculate()
	return JsonResponse(travel_expenses.__dict__)

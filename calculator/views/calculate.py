from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from calculator.services import Calculator


@csrf_exempt
def calculate(request):
	from_date = request.GET.get('from_date', None)
	to_date = request.GET.get('to_date', None)

	from_date = datetime.strptime(from_date, "%Y-%m-%d")
	to_date = datetime.strptime(to_date, "%Y-%m-%d")
	city_code = request.GET.get('city_code', None)

	travel_expenses = Calculator(city_code, from_date, to_date).calculate()
	return JsonResponse(travel_expenses.__dict__)

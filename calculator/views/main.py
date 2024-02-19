from django.http import JsonResponse
from django.shortcuts import render


def calculate(request):
	return render(request, 'main.html')

def toto(request):
	return render(request, 'landing_page.html')

def test(request):
	result = {}
	for key, value in request.headers.items():
		result[key] = value
	print(result)
	return JsonResponse(result)

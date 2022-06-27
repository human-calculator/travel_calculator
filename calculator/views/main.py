from django.shortcuts import render


def calculate(request):
	return render(request, 'main.html')


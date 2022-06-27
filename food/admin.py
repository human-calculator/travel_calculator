from django.contrib import admin
from food.models import FoodPrice


# Register your models here.
class FoodPricdAdmin(admin.ModelAdmin):
	...


admin.site.register(FoodPrice, FoodPricdAdmin)

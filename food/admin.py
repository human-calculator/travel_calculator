from django.contrib import admin
from food.models import FoodPrice


# Register your models here.
class FoodPricdAdmin(admin.ModelAdmin):
	list_display = ('city_code', 'amount', 'updated_at', )


admin.site.register(FoodPrice, FoodPricdAdmin)

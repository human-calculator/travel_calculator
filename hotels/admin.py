from django.contrib import admin
from hotels.models import HotelPrice


# Register your models here.
class HotelPriceAdmin(admin.ModelAdmin):
	list_display = ('city_code', 'check_in_date', "min_price", "max_price", "median_price", 'updated_at', )


admin.site.register(HotelPrice, HotelPriceAdmin)

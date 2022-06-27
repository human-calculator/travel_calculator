from django.contrib import admin
from cities.models import City, Country


# Register your models here.
class CountryAdmin(admin.ModelAdmin):
	list_display = ('eng_name', 'kor_name',)


class CityAdmin(admin.ModelAdmin):
	list_display = ('city_code', 'eng_name', 'kor_name', 'country_kor_name',)

	@admin.display(description='Country')
	def country_kor_name(self, obj):
		return obj.country_id.kor_name


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)

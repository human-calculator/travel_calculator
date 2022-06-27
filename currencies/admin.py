from django.contrib import admin
from currencies.models import Currency


# Register your models here.
class CurrencyAdmin(admin.ModelAdmin):
	list_display = ('cur_unit', 'cur_nm', 'ttb', 'tts', 'deal_bas_r', 'updated_at', )


admin.site.register(Currency, CurrencyAdmin)

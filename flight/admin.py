from django.contrib import admin
from flight.models.flight import FlightSummary


# Register your models here.
class FlightSummaryAdmin(admin.ModelAdmin):
	list_display = ("origin", "destination", "departure_date", "price", "created_at", "updated_at",)
	list_display_links = ("origin", "destination",)


admin.site.register(FlightSummary, FlightSummaryAdmin)

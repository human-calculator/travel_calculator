from django.apps import AppConfig
from calculator.tasks import execute_update_flight_summary_task


class FlightConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'flight'

	def ready(self):
		execute_update_flight_summary_task()

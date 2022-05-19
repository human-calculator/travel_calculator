from django.apps import AppConfig
from calculator.tasks import execute_update_hotel_prices_task


class HotelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotels'
    
    def ready(self):
        execute_update_hotel_prices_task()

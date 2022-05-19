from django.apps import AppConfig

from calculator.tasks import execute_update_currencies_task


class CurrenciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'currencies'
    
    def ready(self):
        execute_update_currencies_task()


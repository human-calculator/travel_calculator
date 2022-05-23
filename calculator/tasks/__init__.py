from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone


seoul_tz = timezone("Asia/Seoul")
scheduler = BackgroundScheduler(timezone=seoul_tz)
scheduler.start()


def execute_update_currencies_task():
	print("execute_update_currencies_task!")
	from calculator.services.currency import CurrencyScheduleManager
	scheduler.add_job(
		CurrencyScheduleManager().execute, 'cron', hour=0, minute=0, second=0, name='execute_update_currencies_task'
	)


def execute_update_hotel_prices_task():
	print('execute_update_hotel_prices_task!')
	from calculator.services.hotel import HotelScheduleManager
	scheduler.add_job(
		HotelScheduleManager().execute, 'cron', hour=0, minute=10, second=0, name='execute_update_hotel_prices_task'
	)


def execute_update_flight_summary_task():
	print('execute_update_flight_summary_task!')
	from flight.services.flight import FlightScheduleManager
	scheduler.add_job(
		FlightScheduleManager().execute(), 'cron', hour=0, minute=20, second=0, name='execute_update_flight_summary_task'
	)

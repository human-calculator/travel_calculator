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

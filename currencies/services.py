import os
import traceback
from datetime import datetime

import requests

from calculator.utils import send_slack
from currencies.models import Currency


class CurrencyScheduleManager:

    def __init__(self):
        self._currency_auth_key = os.getenv("CURRENCY_AUTH_KEY")
        self._today = datetime.today().strftime("%Y%m%d")

    def get_currency(self):
        res = requests.get(
            f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={self._currency_auth_key}&searchdate=20220516&data=AP01")
        return res.json()

    def execute(self):
        try:
            if self._currency_auth_key is None:
                print("currency auth key required!")
                return

            currencies = self.get_currency()
            for currency in currencies:
                update_dict = dict(
                    cur_nm=currency.get("cur_nm"),
                    ttb=self.convert_str_to_float(currency.get("ttb")),
                    tts=self.convert_str_to_float(currency.get("tts")),
                    deal_bas_r=self.convert_str_to_float(currency.get("deal_bas_r"))
                )
                Currency.objects.update_or_create(
                    cur_unit=currency.get("cur_unit").split("(")[0],
                    defaults=update_dict
                )
        except Exception as e:
            err_msg = traceback.format_exc()
            send_slack(f":ghost: [FAILED] [SCHEDULE] [CURRENCY] {err_msg}")

    @staticmethod
    def convert_str_to_float(str_value: str):
        return float(str_value.replace(",", ""))
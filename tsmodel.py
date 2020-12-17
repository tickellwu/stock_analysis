import tushare as ts
import datetime

class date:
    def _get_date(day=datetime.date.today(), _span=365 * 2, format='%Y%m%d'):
        date_list = [day.strftime(format), (day - datetime.timedelta(days=_span)).strftime(format)]
        return date_list

class tsclass:
    def __init__(self, token, date_list=date._get_date()):
        self._token = token
        self._pro = ts.pro_api(token)
        self._date_list = date_list

    def get_daily_data(self, stock_code):
        return self._pro.daily(ts_code=stock_code, end_date=self._date_list[0], start_date=self._date_list[1])

    def get_stock_list(self):
        return self._pro.stock_basic(exchange='', list_status='L')

    def trade_cal(self):
        return self._pro.trade_cal(exchange='', end_date=self._date_list[0], start_date=self._date_list[1])











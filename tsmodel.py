import tushare as ts
import datetime

class date:
    def _get_date(day=datetime.date.today(), _span=365, format='%Y%m%d'):
        date_list = [day.strftime(format), (day - datetime.timedelta(days=_span)).strftime(format)]
        return date_list

class tsclass:
    def __init__(self, token, date_list=date._get_date()):
        self._token = token
        self._pro = ts.pro_api(token)
        self._date_list = date_list

    def daily(self, stock_code):
        return self._pro.daily(ts_code=stock_code, end_date=self._date_list[0], start_date=self._date_list[1])

    def trade_cal(self):
        return self._pro.trade_cal(exchange='', end_date=self._date_list[0], start_date=self._date_list[1])

    def getdata(self, stock_code, date_list=date._get_date(_span=365*2)):
        return self._pro.daily(ts_code=stock_code, end_date=date_list[0], start_date=date_list[1])








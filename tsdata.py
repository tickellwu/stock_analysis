import os
import datetime
import matplotlib.pyplot as plt
from finta import TA
from tsmodel import tsclass
from tickell_log import log

class tsdata:
    def __init__(self, tc: tsclass, code):
        self._tsm = tc
        self._code = code
        self._data = self._tsm.get_daily_data(code)

    def save_pic(self, plt, name):
        path = "tmp" + datetime.date.today().strftime('%Y%m%d')
        if not os.path.exists(path):
            os.mkdir(path)
        plt.savefig(path + '/' + name)
        return

    def rsi(self, engine):
        span = [6, 12, 24]
        data = self._data
        data_copy = data.sort_values(by=['trade_date'])
        for i in range(len(span)):
            name = 'RSI_' + str(span[i])
            data[name] = TA.RSI(data_copy, period=span[i])
        log("info " + " " + self._code + " \n" + str(data))
        try:
            rsi_copy = data.loc[:0]
            rsi_copy.to_sql('data_list', con=engine, if_exists="append")
        except Exception:
            log("err " + " " + self._code + " \m" + str(data))
        return data

    def ma(self):
        span = [5, 10, 30]
        data = self._data
        data["volume"] = data["close"]
        data_copy = data.sort_values(by=['trade_date'])
        plt.figure(figsize=(30, 10))
        for i in range(len(span)):
            name = 'MA_' + str(span[i])
            data[name] = TA.VAMA(data_copy, period=span[i])
            ma = data.sort_values(by=['trade_date'])
            plt.plot(ma["trade_date"][-30:], ma[name][-30:])
        self.save_pic(plt, self._code[:6] + 'RSI.png')
        return data

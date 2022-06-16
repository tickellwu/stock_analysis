# -*- coding: utf-8 -*-

import os
import tsmodel
import tsdata as td
import pandas as pd
import datetime
from tickell_log import log
import Dao
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import save_date_sql

buyed = ["000970.SZ", "600029.SH", "600115.SH", "600297.SH", "600990.SH"]

kBuyed = 1
kRsiLow = 1 << 1
kRsiHigh = 1 << 2
kRsiUp = 1 << 3
kRsiDown = 1 << 4


def save_pic(plt, name):
    path = "tmp" + datetime.date.today().strftime('%Y%m%d')
    if not os.path.exists(path):
        os.mkdir(path)
    plt.savefig(path + '/' + name)
    return


def covert_to_str(ts_stock):
    res = ts_stock["ts_code"] + " "
    res = res + "name:" + str(ts_stock["name"]) + " "
    res = res + "industry:" + str(ts_stock["industry"]) + " "
    res = res + "market:" + str(ts_stock["market"]) + " "
    return res


def get_rsi_diff(rsi, i):
    return rsi["RSI_6"][i] * 2 - rsi["RSI_12"][i] - rsi["RSI_24"][i]


if __name__ == "__main__":
    engine = create_engine('mysql://grafana:1ikedb^R@127.0.0.1:3333/stock_db')
    dao = Dao.sqldao(engine)

    token_file = open("token.key", mode='r')
    token = token_file.read()
    ts = tsmodel.tsclass(token)

    stock_list = ts.get_stock_list()
    #todo update code_list when has new stock
    if datetime.date.today().weekday() == 0:
        stock_list.to_sql('stock_list_info', con=engine, if_exists="replace")

    for code in stock_list["ts_code"]:
        log("start " + code)
        data = td.tsdata(ts, code)
        rsi = data.rsi(engine)
        if rsi.size < 30:
            continue
        status = 0

        if code in buyed:
            status = status | kBuyed
        if rsi["RSI_6"][0] < 15:
            status = status | kRsiLow
        if get_rsi_diff(rsi, 0) >= 0 and get_rsi_diff(rsi, 1) < 0:
            status = status | kRsiUp
        if rsi["RSI_6"][0] > 85:
            status = status | kRsiHigh
        if get_rsi_diff(rsi, 0) <= 0 and get_rsi_diff(rsi, 1) > 0:
            status = status | kRsiDown
        log("set status" + code + ":" + str(status))
        dao.set_status(code, status)
        # ma = data.ma()
    last_day = pd.DataFrame({'name': ['last_day', 'last_day_before'],
                             'date': [rsi["trade_date"][0], rsi["trade_date"][1]]})
    # print(last_day)
    last_day.to_sql('day_list', con=engine, if_exists="replace")


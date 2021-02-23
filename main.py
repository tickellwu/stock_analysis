# -*- coding: utf-8 -*-

import os
import tsmodel
import tsdata as td
import datetime
from tickell_log import log
from sqlalchemy import create_engine
#import save_date_sql

buyed = ["000970.SZ", "600029.SH", "600115.SH", "600297.SH", "600990.SH"]

DB_IP = "192.168.2.26"
DB_PORT = 3333
DB_USERNAME = "grafana"
DB_PASSWD = "1ikedb^R"
DB_DBNAME = "stock_db"
#db = MySQLdb.connect(host = DB_IP, port = DB_PORT, user = DB_USERNAME, passwd = DB_PASSWD, db = DB_DBNAME, charset = "utf8")

buyed = ["000970.SZ", "600029.SH", "600115.SH", "600297.SH", "600990.SH"]

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

if __name__=="__main__":
    engine = create_engine('mysql://grafana:1ikedb^R@127.0.0.1:3333/stock_db')

    token_file = open("token.key", mode='r')
    token = token_file.read()
    ts = tsmodel.tsclass(token)

    stock_list= ts.get_stock_list()
    if datetime.date.today().weekday() == 0:
        stock_list.to_sql('stock_list_info', con=engine)

    #print(str(ts.get_stock_list().iloc[1]))
    resault_code = []
    resault_code1 = []
    resault_code2 = []
    i = 0

    for code in stock_list["ts_code"]:
        log("start " + code)
        data = td.tsdata(ts, code)
        rsi = data.rsi(engine)
        if rsi.size < 30:
            i = i + 1
            continue
        t_day_rsi6 = rsi["RSI_6"][0]
        if t_day_rsi6 < 15:
            print(code, covert_to_str(ts.get_stock_list().loc[i]))
            resault_code.append(covert_to_str(ts.get_stock_list().loc[i]) + "\n")
        if t_day_rsi6 * 2 - rsi["RSI_12"][0] - rsi["RSI_24"][0] >= 0 and  rsi["RSI_6"][1] * 2 - rsi["RSI_12"][1] - rsi["RSI_24"][1] <= 0 :
            print(code,covert_to_str(ts.get_stock_list().loc[i]))
            resault_code1.append(covert_to_str(ts.get_stock_list().loc[i]) + "\n")
        if code in buyed:
            if t_day_rsi6 > 85 or (t_day_rsi6 * 2 - rsi["RSI_12"][0] - rsi["RSI_24"][0] <= 0 and
                                   rsi["RSI_6"][1] * 2 - rsi["RSI_12"][1] - rsi["RSI_24"][1] >= 0):
                print(code, covert_to_str(ts.get_stock_list().loc[i]))
                resault_code2.append(covert_to_str(ts.get_stock_list().loc[i]) + "\n")

        i = i + 1
        #ma = data.ma()
    fo = open("resalt.txt", "w")
    fo.writelines(resault_code)
    fo.close()
    fo1 = open("resalt1.txt", "w")
    fo1.writelines(resault_code1)
    fo1.close()
    fo2 = open("resalt2.txt", "w")
    fo2.writelines(resault_code2)
    fo2.close()




# -*- coding: utf-8 -*-

import os
import tsmodel
import tsdata as td
import datetime

def save_pic(plt, name):
    path = "tmp" + datetime.date.today().strftime('%Y%m%d')
    if not os.path.exists(path):
        os.mkdir(path)
    plt.savefig(path + '/' + name)
    return

if __name__=="__main__":
    token_file = open("token.key", mode='r')
    token = token_file.read()
    ts = tsmodel.tsclass(token)
    #code = '600519.SH'
    #code = '002233.SZ'
    code = '002230.SZ'
    data = td.tsdata(ts, code)
    data.rsi()
    data.ma()





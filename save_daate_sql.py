# -*- coding: utf-8 -*-
#!/usr/bin/python

import requests
import sys
import json
import MySQLdb
import time

DB_IP="103.216.103.184"
DB_PORT=5201
DB_USERNAME="myshard"
DB_PASSWD="myshard"
DB_DBNAME="myshard"

flog = open("fb.log", "a+")

db = MySQLdb.connect(host=DB_IP,port=DB_PORT,user=DB_USERNAME,passwd=DB_PASSWD,db=DB_DBNAME,charset="utf8")
cursor = db.cursor()

class fbinfo:
    def __init__(self, _name, _type):
        self.fb_name = _name
        self.fb_type = _type

def savedata(file, row):
    datasqlstr = 'update third_party_user set user_id = ' + row[1] + ' type = ' + str(row[2]) + ' where uid = ' + str(row[0]) + ' and user_id like ' + '\"fb%\"' + ' and token = \"%s\"'%(row[3])
    file.write(datasqlstr + '\n')
    file.flush()

def log(str):
    flog.write(time.asctime(time.localtime(time.time())) + "  " + str + '\n')
    flog.flush()

fbappid2str = {'655018784691173': 'fb', '355677601673935': 'fb3', '419985648717362': 'fb4', '854438984952910': 'fb6', '690806725036137': 'fb7'}
fbappid2int = {'655018784691173': 1, '355677601673935': 67, '419985648717362': 68, '854438984952910': 74, '690806725036137': 76}

def getfbdata(token):
    url = "https://graph.facebook.com/v9.0/me?fields=id,ids_for_business&debug=all&access_token=" + token
    #print url
    r = requests.get(url)
    #print r.status_code
    log(r.content)
    return r

def getinfo(token):
    resalt = getfbdata(token)
    fb_info = fbinfo("", 0)
    if resalt.status_code == 200:
        datajson = json.loads(resalt.content)
        #print datajson
        id = datajson["id"]
        appinfo = datajson["ids_for_business"]["data"]
        for i in appinfo:
            if i["id"] == id:
                appid = i["app"]["id"]
                fb_info.fb_name = fbappid2str[appid] + "_" + id
                fb_info.fb_type = fbappid2int[appid]
    log("%s, %u"%(fb_info.fb_name, fb_info.fb_type))
    return fb_info

def sql_option(_sqlstr, option):
    log(_sqlstr)
    try:
        cursor.execute(_sqlstr)
        db.commit()
    except Exception, e:
        print e
        db.close()
        exit("sql_option error " + _sqlstr)
        return ()
    results = cursor.fetchall()
    log(option + " sql size:%u result:%s" %(len(results), str(results)))
    return results



fsave = open("data.txt", "a+")
fo = open("test.csv", "rw+")
line = fo.readline()
while line is not None and line != '':
    uid = line.split()[0]
    sqlstr = 'select uid, user_id, type, token from third_party_user where uid = ' + uid + ' and user_id like ' + '\"fb%\"'
    results = sql_option(sqlstr, "get")

    if len(results) == 0:
        log("ERR conn't find " + uid)
    for row in results:
        token = row[3]
        third_type = int(row[2])
        user_id = row[1]
        fb_info = getinfo(token)
        if fb_info.fb_type == 0:
            log("ERR get fb info fail uid: " + uid)
            continue
        if fb_info.fb_name != user_id or fb_info.fb_type != third_type:
            savedata(fsave, row)
            checksql = 'select count(*) from third_party_user where user_id =  \"%s\"' % (fb_info.fb_name)
            checkresults = sql_option(checksql, "get1")
            if checkresults[0][0] == 0:
                #if len(checkresults) == 0:
                newsql = 'update third_party_user set user_id = \"%s\", type = %u where uid = %s and token = \"%s\"' % (fb_info.fb_name, fb_info.fb_type, uid, token)
                try:
                    cursor.execute(newsql)
                    db.commit()
                    log("Notice affected rows = %u" % cursor.rowcount)
                except Exception, e:
                    print e
            else:
                newsql = "delete third_party_user where user_id = %s and uid = %s " % (user_id, uid)
                log("Notice third user:" + fb_info.fb_name + " exist Manual process uid:" + uid)
            log(newsql)
            #check results
            sql_option(sqlstr, "check")
    log("finisht uid " + uid)

    time.sleep(0.01)
    line = fo.readline()
fsave.close()
fo.close()
flog.close()


y
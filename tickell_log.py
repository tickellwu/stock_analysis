import datetime
import time


file = "log/" + datetime.date.today().strftime('%Y_%m_%d') + ".log"
flog = open(file, "a+")

def log(str):
    flog.write(time.asctime(time.localtime(time.time())) + "  " + str + '\n')
    flog.flush()

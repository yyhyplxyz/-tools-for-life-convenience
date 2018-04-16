#coding=utf8
import itchat
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import threading
import random
import logging

#发送个特定消息到某公众号
def job1():
    mps = itchat.get_mps()
    mps = itchat.search_mps(name=u'中东安协')
    userName = mps[0]['UserName']
    itchat.send("hello",toUserName = userName)

#这个函数是时不时发送些消息，防止长时间连接微信，又没有任何活动出错的。
#当然了，也有可能不会出错
def send_message_task():
    delay = random.randint(3, 6)
    print(delay)
    time.sleep(delay)
    try:
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        msg = 'Delay: ' + str(delay) + 's\n' + 'Time: ' + time_str
        itchat.send(msg, toUserName=u'小子')
    except:
         print "Unexpected error:", sys.exc_info()[0]


itchat.auto_login(hotReload=True)
#下面这段代码是为了防止apscheduler库出问题的，stackoverflow里说的，我不太清楚什么原理
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)
#开两个线程，分别完成工作
send_message_task()
scheduler = BlockingScheduler()
scheduler.add_job(send_message_task, 'interval', seconds=10, args=[])
scheduler.add_job(job1, 'date', run_date=datetime.datetime(2018, 4, 16, 11, 40, 5), args=[])
scheduler.start()

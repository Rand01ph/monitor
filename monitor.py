#!/usr/bin/env python
# encoding: utf-8

import threading
import pymysql
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from log import logger


def get_con():
    host = "127.0.0.1"
    port = 3306
    ridersdb = "zhuanche"
    user = "root"
    password = "root"
    con = pymysql.connect(host=host, user=user, passwd=password, db=ridersdb, port=port, charset="utf8")
    return con


def calculate_time():

#    now = time.mktime(datetime.now().timetuple())-60*10
    now = time.mktime(datetime.now().timetuple())
    result = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
    return result


def get_data():
    select_time = calculate_time()
    logger.info("select time:"+select_time)
    sql = "SELECT * FROM riders WHERE status=0 OR (status=1 and updated < now()-02000000);"
#SELECT * FROM riders WHERE status=0 OR (status=1 and updated < now()-090000);
    conn = get_con()

    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


def send_email(content):

    sender = "tanyawei@126.com"
    receiver = ["361212419@qq.com"]
    host = 'smtp.126.com'
    port = 465
    msg = MIMEText(content)
    msg['From'] = "tanyawei@126.com"
    msg['To'] = "361212419@qq.com"
    msg['Subject'] = "Account Error"

    try:
        smtp = smtplib.SMTP_SSL(host, port)
        smtp.login(sender, '********')
        smtp.sendmail(sender, receiver, msg.as_string())
        logger.info("send email success")
    except Exception, e:
        logger.error(e)


def task():
    while True:
        logger.info("monitor running")
        results = get_data()
        if results is not None and len(results) < 10:
            content = "账号问题"
            logger.info("so little to use,so send mail")
            print 'error'
            #  for r in results:
                #  content += r[1]+'\n'
            content += '请尽快补充账号'
            send_email(content)
        time.sleep(10*60)


def run_monitor():
    monitor = threading.Thread(target=task)
    monitor.start()


if __name__ == "__main__":
  run_monitor()

#!/usr/bin/env python
# encoding: utf-8

import pymysql
import sys
import os
import time

nowtime = str(time.strftime('%Y-%m-%d %H:%M:%S'))

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='zhuanche_dev')

cur = conn.cursor()

infile = sys.argv[1]
test = []
with open(infile, 'r') as f:
    for line in f.readlines():
        result = line.strip().split(',')[2:7]
        result.append(nowtime)
        cur.execute("""insert into riders (username, password, alipay_account, alipay_login_pass, alipay_pay_pass, created) values (%s, %s, %s, %s, %s, %s);""", tuple(result))

conn.close()

#!/usr/bin/env python
# encoding: utf-8

import pymysql
import sys
import os

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='zhuanche')

cur = conn.cursor()

cur.execute("SELECT username, password FROM riders WHERE status=2")

outfile = sys.argv[1]

with open(outfile, 'a') as f:
    for r in cur.fetchall():
        f.write(','.join(r))
        f.write(os.linesep)

conn.close()

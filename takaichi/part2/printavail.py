#!/usr/bin/python3

import sqlite3
import datetime

now = datetime.datetime.now()
old = now + datetime.timedelta(minutes=-90)

try: 
    cn = sqlite3.connect("/home/user/takaichi/takaichi.db")
    cs = cn.cursor()

    cs.execute('''
        select date from feeds 
        where used = 0 and date >= ? 
    ''', (old.strftime("%Y-%m-%d-%H%M"),))
    rs = cs.fetchall()
    num_fresh = len(rs)

    cs.execute('''
        select date from feeds 
        where used = 0 and date < ? 
    ''', (old.strftime("%Y-%m-%d-%H%M"),))
    rs = cs.fetchall()
    num_old = len(rs)

    print("fresh: " + str(num_fresh) + " ; OLD(-90 min): " + str(num_old))

except Exception as e: 
    print(e)
finally: 
    cn.close();


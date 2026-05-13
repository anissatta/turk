#!/usr/bin/python3

import sqlite3
import html

try: 
    cn = sqlite3.connect("/home/user/takaichi/takaichi.db")
    cs = cn.cursor()

    cs.execute('''
        select * from log 
        order by date DESC 
        limit 30
    ''')
    logs = cs.fetchall()
#    is_first = True
    for log in logs: 
        print("<li>" + html.escape(log[1], quote=True) + "</li>")

except Exception as e: 
    print(e)
finally: 
    cn.close();


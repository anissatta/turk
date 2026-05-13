#!/usr/bin/python3

import subprocess
import datetime
import sqlite3
import random

def get_links(page): 
    res = subprocess.run(["/home/user/takaichi/yoripan/yoripan-getlink.sh", str(page)], capture_output=True, text=True)
    return res.stdout.split("\n")

try: 
    cn = sqlite3.connect("/home/user/takaichi/yoripan/yoripan.db")
    cs = cn.cursor()

    cs.execute('''
        create table if not exists yoripan (
            url text primary key, 
            date text not null, 
            page text not null, 
            used integer
        )
    ''')

    now = datetime.datetime.now()
    # this is NOT their published date. 
    date = now.strftime("%Y-%m-%d-%H%M")

    # 1. try the first page. 
    for link in get_links(1): 
        if (len(link) < 10): 
            # my be not valid. 
            pass
        else: 
            cs.execute('''
                insert or ignore into yoripan 
                (url, date, page, used) 
                values (?, ?, ?, ?)
            ''', 
            (link, date, "1", 0))
    # 2. then a random one. 
    r = random.randint(2, 777)
    for link in get_links(str(r)): 
        if (len(link) < 10): 
            # my be not valid. 
            pass
        else: 
            cs.execute('''
                insert or ignore into yoripan 
                (url, date, page, used) 
                values (?, ?, ?, ?)
            ''', 
            (link, date, str(r), 0))

    # 3. now, let us pick one of 'em... 
    cs.execute('''
        select * from yoripan 
        where used = 0 
        order by page ASC 
        limit 1
    ''')
    feeds = cs.fetchall()

    if (len(feeds) == 0): 
        # oh... 
        subprocess.run(["/home/user/takaichi/yoripan/yoripan-createpan.sh", ""])
    else: 
        feed = feeds[0]
        f_key = feed[0]
        f_url = "https://www.10000recipe.com" + f_key
        subprocess.run(["/home/user/takaichi/yoripan/yoripan-createpan.sh", f_url])
        cs.execute('''
            update yoripan set used = 1 
            where url = ? 
        ''', 
        (f_key,))

    cn.commit();
except Exception as e: 
    print(e)
    cn.rollback();
finally: 
    cn.close();

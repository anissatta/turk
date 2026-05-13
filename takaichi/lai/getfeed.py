#!/usr/bin/python3

import datetime
import sqlite3
import feedparser
import subprocess

feed_urls = [
    "https://feeds.feedburner.com/rsscna/politics",
    "https://feeds.feedburner.com/rsscna/intworld",
    "https://feeds.feedburner.com/rsscna/mainland",
    "https://feeds.feedburner.com/rsscna/finance",
    "https://feeds.feedburner.com/rsscna/technology",
    "https://feeds.feedburner.com/rsscna/lifehealth",
    "https://feeds.feedburner.com/rsscna/social",
    "https://feeds.feedburner.com/rsscna/local",
    "https://feeds.feedburner.com/rsscna/culture",
    "https://feeds.feedburner.com/rsscna/sport",
    "https://feeds.feedburner.com/rsscna/stars"
]

now = datetime.datetime.now()

try: 
    cn = sqlite3.connect("lai.db")
    cs = cn.cursor()

    cs.execute('''
        create table if not exists feeds (
            url text primary key, 
            title text not null, 
            date text not null, 
            used integer
        )
    ''')

    # this is NOT their published date. 
    date = now.strftime("%Y-%m-%d-%H%M")
    for feed_url in feed_urls: 
        f = feedparser.parse(feed_url)
        for entry in f.entries: 
            cs.execute('''
                insert or ignore into feeds 
                (url, title, date, used) 
                values (?, ?, ?, ?)
            ''', 
            (entry.link, entry.title, date, 0))

    cs.execute('''
        select * from feeds 
        where used = 0 
        order by date DESC
        limit 1
    ''')
    res = cs.fetchall()
    if (len(res) == 0): 
        feed = feedparser.parse("https://feeds.feedburner.com/rsscna/politics").entries[0]
        f_url = feed.link
        f_title = feed.title
    else: 
        f_url = res[0][0]
        f_title = res[0][1]
        cs.execute('''
            update feeds set used = 1 
            where url = ? 
        ''', 
        (f_url,))

    dago = now + datetime.timedelta(days=-1)
    cs.execute('''
        delete from feeds 
        where date < ? 
   ''', (dago.strftime("%Y-%m-%d-%H%M"),))

    now = datetime.datetime.now()
    old = now + datetime.timedelta(minutes=-90)

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

    print(f_url)
    print(f_title)
    subprocess.run(["/home/user/takaichi/lai/part1/getfed.sh", f_url, f_title, str(num_fresh), str(num_old)])

    cn.commit();
    print('OK')
except Exception as e: 
    print(e)
    cn.rollback();
finally: 
    cn.close();


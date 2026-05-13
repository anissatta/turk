#!/usr/bin/python3

import sys
import datetime
import sqlite3
import feedparser
import subprocess
import random

feed_urls = [
    "https://news.yahoo.co.jp/rss/topics/top-picks.xml",
    "https://news.yahoo.co.jp/rss/topics/domestic.xml",
    "https://news.yahoo.co.jp/rss/topics/world.xml",
    "https://news.yahoo.co.jp/rss/topics/business.xml",
    "https://news.yahoo.co.jp/rss/topics/entertainment.xml",
    "https://news.yahoo.co.jp/rss/topics/sports.xml",
    "https://news.yahoo.co.jp/rss/topics/it.xml",
    "https://news.yahoo.co.jp/rss/topics/science.xml",
    "https://news.yahoo.co.jp/rss/topics/local.xml"
]

now = datetime.datetime.now()
generation = 0
if len(sys.argv) > 1:
    generation = int(sys.argv[1])

try: 
    cn = sqlite3.connect("takaichi.db")
    cs = cn.cursor()

    cs.execute('''
        create table if not exists feeds (
            url text primary key, 
            title text not null, 
            date text not null, 
            used integer
        )
    ''')

    cs.execute('''
        create table if not exists log (
            url text not null, 
            title text not null, 
            date text primary key
        )
    ''')

    # this is for a fallback. 
    feed_url = feed_urls[generation % len(feed_urls)]
    f = feedparser.parse(feed_url)
    # this is NOT their published date. 
    date = now.strftime("%Y-%m-%d-%H%M")

    # 26. 5. 7 
    extras = [
        "https://news.yahoo.co.jp/rss/categories/domestic.xml",
        "https://news.yahoo.co.jp/rss/categories/world.xml",
        "https://news.yahoo.co.jp/rss/categories/business.xml",
        "https://news.yahoo.co.jp/rss/categories/entertainment.xml",
        "https://news.yahoo.co.jp/rss/categories/sports.xml",
        "https://news.yahoo.co.jp/rss/categories/it.xml",
        "https://news.yahoo.co.jp/rss/categories/science.xml",
        "https://news.yahoo.co.jp/rss/categories/life.xml",
        "https://news.yahoo.co.jp/rss/categories/local.xml",
        #"https://www.asahi.com/rss/asahi/newsheadlines.rdf",
        #"https://www.asahi.com/rss/asahi/international.rdf",
        "https://business.nikkei.com/rss/sns/nb.rdf",
        "https://news.ntv.co.jp/rss/index.rdf",
        "https://news.web.nhk/n-data/conf/na/rss/cat0.xml"
    ]
    random.shuffle(extras)
    for i in range(5): 
        ext = extras[i]
        f2 = feedparser.parse(ext)
        for entry in f2.entries: 
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
        feed = f.entries[0]
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

    subprocess.run(["./part1/getfed.sh", f_url, f_title])
    subprocess.run(["./part2/getfed.sh", f_url, f_title])

    # write log! 
    cs.execute('''
        insert or ignore into log 
        (url, title, date) 
        values (?, ?, ?)
    ''', 
    (f_url, f_title, date))

    dago = now + datetime.timedelta(days=-1)
    cs.execute('''
        delete from feeds 
        where date < ? 
   ''', (dago.strftime("%Y-%m-%d-%H%M"),))
    cs.execute('''
        delete from log 
        where date < ? 
   ''', (dago.strftime("%Y-%m-%d-%H%M"),))

    cn.commit();
    print('OK')
except Exception as e: 
    print(e)
    cn.rollback();
finally: 
    cn.close();


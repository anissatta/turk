#!/usr/bin/python3

import sqlite3
import html
from janome.tokenizer import Tokenizer

try: 
    cn = sqlite3.connect("/home/user/takaichi/takaichi.db")
    cs = cn.cursor()

    cs.execute('''
        select * from feeds 
        where used = 0 
        order by date DESC 
        limit 21
    ''')
    logs = cs.fetchall()
    t = Tokenizer()
    for log in logs: 
        text = log[1]
        li = ""
        i = 1
        for tok in t.tokenize(text, wakati=True): 
            if ("高市" in tok or tok == "トランプ"): 
                li = li + '<span class="taka">' + html.escape(tok, quote=True) + '</span>'
            else: 
                if (i % 2 == 0): 
                    li = li + '<span class="even">' + html.escape(tok, quote=True) + '</span>'
                else: 
                    li = li + '<span class="odd">' + html.escape(tok, quote=True) + '</span>'
            i = i + 1
        print("<li>" + li + "</li>")

except Exception as e: 
    print(e)
finally: 
    cn.close();


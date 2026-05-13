#!/usr/bin/python3

import sys
from janome.tokenizer import Tokenizer
import sqlite3
import html

lst = []
def addListIfNew(item): 
    if (item in lst): 
        pass
    else: 
        lst.append(item)

def yum(text): 
    li = ""
    t = Tokenizer()
    i = 1
    for tok in t.tokenize(text, wakati=True): 
        if (i % 2 == 0): 
            li = li + '<span class="even">' + html.escape(tok, quote=True) + '</span>'
        else: 
            li = li + '<span class="odd">' + html.escape(tok, quote=True) + '</span>'
        i = i + 1
    return li

if (len(sys.argv) == 2): 
    ret = ''
    text = sys.argv[1]
    t = Tokenizer()
    for tok in t.tokenize(text): 
        if (tok.part_of_speech.split(',')[0] == '名詞'): 
            addListIfNew(tok.base_form)

    try: 
        cn = sqlite3.connect("/home/user/takaichi/takaichi.db")
        cs = cn.cursor()
        for kw in lst[:5]: 
            ret = ret + '<h3>' + html.escape(kw, quote=True) + '</h3>'
            ret = ret + '<ul>'
            cs.execute('''
                select title from feeds 
                where title like '%'''
                + kw + 
                '''%'
                order by random() 
                limit 3
            ''')
            recs = cs.fetchall()
            for rec in recs: 
                ret = ret + '<li>' + yum(rec[0]) + '</li>'
            ret = ret + '</ul>'
    except Exception as e: 
        print(e)
    finally: 
        cn.close();

    print(ret)


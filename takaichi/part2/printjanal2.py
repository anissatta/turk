#!/usr/bin/python3

import sys
from janome.tokenizer import Tokenizer
import subprocess

def trans(base): 
    res = subprocess.run(["trans", "-b", "ja:en", base], capture_output=True, text=True)
    return res.stdout

def is_ok(text): 
    # it mustn't be '-' or '-something' for it'll be recognized as an option by trans command. 
    #if ('-' in text): 
    #    return False
    #else: 
    #    return True
    # OK let's accept multibytes only. 
    if (len(text.encode('utf-8')) > len(text)): 
        return True
    else: 
        return False

if (len(sys.argv) == 2): 
    ret = ''
    text = sys.argv[1]
    t = Tokenizer()
    i = 1
    for tok in t.tokenize(text): 
        if (i % 2 == 0): 
            ret += '<ruby class="even">' + tok.surface
        else: 
            ret += '<ruby class="odd">' + tok.surface
        if (tok.part_of_speech.split(',')[0] == '名詞' and is_ok(tok.base_form)): 
            ret += '<rt>' + trans(tok.base_form) + '</rt>'
        ret += '</ruby>'
        i = i + 1
    print(ret)


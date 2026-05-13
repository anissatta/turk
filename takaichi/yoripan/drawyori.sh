#!/bin/sh

/home/user/takaichi/yoripan/yoripan.py > /home/user/takaichi/yoripan/core
#cat /home/user/takaichi/yoripan/heada.html /home/user/takaichi/yoripan/bg.uri /home/user/takaichi/yoripan/headb.html /home/user/takaichi/yoripan/core /home/user/takaichi/yoripan/tail.html > /home/user/takaichi/yoripan/index.html
cat /home/user/takaichi/yoripan/head.html /home/user/takaichi/yoripan/core /home/user/takaichi/yoripan/tail.html > /home/user/takaichi/yoripan/index.html
wkhtmltoimage --width 800 --crop-h 165 /home/user/takaichi/yoripan/index.html /home/user/takaichi/yoripan/yori.png


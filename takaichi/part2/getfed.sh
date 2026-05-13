#!/bin/sh

dest="part2/core"
url="${1}"
tit="${2}"

echo > $dest
echo "<p id='biglogo'>" >> $dest
nice ./part2/printjanal2.py "${tit}" >> $dest
echo "</p>" >> $dest

echo "<p>" >> $dest
/home/user/takaichi/part2/printavail.py >> $dest
echo "</p>" >> $dest

#echo "<ul>" >> $dest
#/home/user/takaichi/part2/printfresh3.py >> $dest
#echo "</ul>" >> $dest
nice ./part2/similar.py "${tit}" >> $dest

### additional 
#nice ./part2/similar.py "${tit}" > part2/similar/core


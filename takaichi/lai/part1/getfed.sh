#!/bin/sh

dest="/home/user/takaichi/lai/part1/core"
url="${1}"
tit="${2}"
num_fre="${3}"
num_old="${4}"
echo "${url}" > /home/user/takaichi/yori.url

do_trans() {
    trans -b "zh-TW:${1}" "${tit}" || trans -b "zh-TW:${1}" "${tit}" || trans -b "zh-TW:${1}" "${tit}"
}

echo "" > $dest

echo '<div class="row">' >> $dest
echo '<div class="col-sm-2">' >> $dest
echo '<div id="qrcode"></div>' >> $dest
echo '</div>' >> $dest
# get thumbnail of this. 
iurl=$(curl -s "${url}" | pup "meta[property=og:image] attr{content}")
wget "${iurl}" -O cna-temp.jpg
convert -strip cna-temp.jpg cna-temp.png
imgdata=$(echo "data:image/png;base64,$(base64 -w 0 cna-temp.png)")
# get the title. 
ktit=$(do_trans ko)
jtit=$(do_trans ja)
echo '<div class="col-sm-7">' >> $dest
echo "<p lang=\"zh-hant\">${tit}</p>" >> $dest
echo "<p lang=\"ko\">${ktit}</p>" >> $dest
echo "<p lang=\"ja\">${jtit}</p>" >> $dest
echo "<p id=\"url\">${url}</p>" >> $dest
echo '</div>' >> $dest
echo '<div class="col-sm-2">' >> $dest
echo "<img src=\"${imgdata}\">" >> $dest
echo '</div>' >> $dest

echo '<div class="col-sm-1">' >> $dest
echo "<p>${num_fre}</p>" >> $dest
echo "<p>${num_old}</p>" >> $dest
echo '</div>' >> $dest


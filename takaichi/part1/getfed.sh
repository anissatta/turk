#!/bin/sh

dest="part1/core"
url="${1}"
tit="${2}"

do_trans() {
    ./trans -b "ja:${1}" "${tit}" || ./trans -b "ja:${1}" "${tit}" || ./trans -b "ja:${1}" "${tit}"
}

nice ./newsis.sh "${url}"

echo > $dest
echo "<ul>" >> $dest
#echo "<li>${tit}</li>" >> $dest
echo "<li>$(do_trans ko)</li>" >> $dest
echo "<li>$(do_trans en)</li>" >> $dest
echo "<li>$(do_trans tl)</li>" >> $dest
echo "<li>$(do_trans vi)</li>" >> $dest
echo "<li>$(do_trans th)</li>" >> $dest
echo "<li>$(do_trans km)</li>" >> $dest
echo "<li>$(do_trans id)</li>" >> $dest
echo "<li>$(do_trans es)</li>" >> $dest
echo "<li>$(do_trans ru)</li>" >> $dest
echo "<li>$(do_trans zh-TW)</li>" >> $dest
echo "</ul>" >> $dest
echo "<p id='url'>" >> $dest
echo "${url}" >> $dest
echo "</p>" >> $dest


#!/bin/bash

url=$1

#printart() {
#    ARTIN=0
#    while read -r line; do
#        if [[ $ARTIN == 1 ]]; then
#            echo $line
#        fi
#
#        if [[ $line == *"• 크게"* ]]; then
#            ARTIN=1
#        fi
#        if [[ $ARTIN == 1 && $line == *"Copyright"* ]]; then
#            break
#        fi
#    done < <(w3m -dump $url)
#}
#convert newsis_base.png -font ./korean1.ttf -gravity North +antialias -pointsize 22 -stroke black -fill black -annotate +0+0 "$(printart | grep -oE ".{1,50}")" bot_temp.png

imgurl=$(curl -s "${url}"|pup 'meta[property="og:image"] attr{content}')
wget "${imgurl}" --timeout 10 -O tmp_newsis.jpg || wget "${imgurl}" --timeout 3 -O tmp_newsis.jpg || wget "${imgurl}" --timeout 3 -O tmp_newsis.jpg
#convert tmp_newsis.jpg -monochrome tmp_newsis.jpg
nice convert tmp_newsis.jpg -resize 320x192! -wave 2x23 newsis.png
nice convert newsis.png -alpha set -channel A -evaluate set 60% newsis.png

# glasses 
mv glass3.png glass4.png
mv glass2.png glass3.png
mv glass1.png glass2.png
mv glass0.png glass1.png
cp newsis.png glass0.png


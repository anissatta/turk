#!/bin/bash

url=$1
#wti=$(w3m -dump https://oilprice.com/ | grep "WTI Crude" | head -n 1)
#kdate=$(echo " $(date "+%y. %m. %d") ${dow}요일 ")
echo "${url}" > /home/user/takaichi/yori.url

if [ -z $url ]; then
#    echo '<p lang="ko">'
#    echo "<strong> ${kdate} </strong>"
#    echo '</p>'
    echo '<p lang="ko">'
    echo $(printop)
    echo '</p>'
else
    #echo '<p><em>'
    #echo "${wti} </em><strong> ${kdate} </strong>"
    #echo '</p>'
    #echo '<p lang="ko">'
    #echo '나에겐 화석 기름보다 참기름이 중요한다. 자, 오늘도 요리를 하자!'
    #echo '</p>'
    echo '<div class="row">'
    echo '<div class="col-sm-2">'
    echo '<div id="qrcode"></div>'
    echo '</div>'
    # get thumbnail of this. 
    iurl=$(curl -s "${url}" | pup "meta[property=og:image] attr{content}")
    wget "${iurl}" -O yoripan-temp.jpg
    convert -strip yoripan-temp.jpg yoripan-temp.png
    imgdata=$(echo "data:image/png;base64,$(base64 -w 0 yoripan-temp.png)")
    # get the title. 
    ktit=$(curl -s "${url}" | pup "meta[property=og:title] attr{content}")
    ctit=$(trans -b ko:zh-TW "${ktit}" || trans -b ko:zh-TW "${ktit}" || trans -b ko:zh-TW "${ktit}")
    etit=$(trans -b ko:ja "${ktit}" || trans -b ko:ja "${ktit}" || trans -b ko:ja "${ktit}")
    echo '<div class="col-sm-7">'
    echo "<p lang=\"ko\">${ktit}</p>"
    echo "<p lang=\"zh-hant\">${ctit}</p>"
    echo "<p lang=\"en\">${etit}</p>"
    echo "<p id=\"url\">${url}</p>"
    echo '</div>'
    echo '<div class="col-sm-3">'
    echo "<img src=\"${imgdata}\">"
    echo '</div>'
fi


#!/bin/bash

degree2() {
    case $((${1}%8)) in
    0)
        echo -0.8
        ;;
    1)
        echo -0.4
        ;;
    2)
        echo -0
        ;;
    3)
        echo 0.4
        ;;
    4)
        echo 0.8
        ;;
    5)
        echo 0.4
        ;;
    6)
        echo 0
        ;;
    7)
        echo -0.4
        ;;
    *)
        echo 0
        ;;
    esac
}

degreeA() {
    case $((${1}%12)) in
    0)
        echo "-60"
        ;;
    1)
        echo "-40"
        ;;
    2)
        echo "-20"
        ;;
    3)
        echo "+0"
        ;;
    4)
        echo "+20"
        ;;
    5)
        echo "+40"
        ;;
    6)
        echo "+60"
        ;;
    7)
        echo "+40"
        ;;
    8)
        echo "+20"
        ;;
    9)
        echo "+0"
        ;;
    10)
        echo "-20"
        ;;
    11)
        echo "-40"
        ;;
    *)
        echo "+0"
        ;;
    esac
}

kdate () {
    dow=""

    case $(date "+%u") in
    1)
        dow="월"
        ;;
    2)
        dow="화"
        ;;
    3)
        dow="수"
        ;;
    4)
        dow="목"
        ;;
    5)
        dow="금"
        ;;
    6)
        dow="토"
        ;;
    7)
        dow="일"
        ;;
    *)
        dow="?"
        ;;
    esac

    echo $(date "+%y. %m. %d ${dow}요일 %H:%M ")
}

upload_via_ftp () {
    # place your own code which uploads the file ($1) 
    # to yours.  
}

i=1

while true
do
    echo $i
    nice ./getfeed.py $i

    # logo 
    cat part2/head.html part2/core part2/tail.html > part2/index.html
    nice wkhtmltoimage --crop-w 800 --height 1400 part2/index.html part2.png
    nice convert part2.png -transparent white -background 'rgba(0,0,0,0)' -rotate $(degree2 $i) part2.png

    #nice composite -gravity NorthWest -geometry +800+0 newsis.png exp1.jpg exp1.jpg
    cp dummies/$(printf %03d $(($i%131))).jpg exp1.jpg
    nice composite -gravity NorthWest -geometry +0+0 part2.png exp1.jpg exp1.jpg

    # glasses 
    nice composite -gravity NorthEast -geometry "$(degreeA $(($i+0)))+0"   glass0.png exp1.jpg exp1.jpg
    nice composite -gravity NorthEast -geometry "$(degreeA $(($i+1)))+192" glass1.png exp1.jpg exp1.jpg
    nice composite -gravity NorthEast -geometry "$(degreeA $(($i+2)))+384" glass2.png exp1.jpg exp1.jpg
    nice composite -gravity NorthEast -geometry "$(degreeA $(($i+3)))+576" glass3.png exp1.jpg exp1.jpg
    nice composite -gravity NorthEast -geometry "$(degreeA $(($i+4)))+768" glass4.png exp1.jpg exp1.jpg

    # time 
    nice convert exp1.jpg -font ./korean1.ttf -gravity North -pointsize 50 -stroke black -fill orange -annotate +0+30 "$(kdate)" exp1.jpg

    # 26. 5. 7 
    convert -resize x360 exp1.jpg exp1-mini.jpg

    # exp2... 
    echo "data:image/png;base64,$(base64 -w 0 glass0.png)" > bg-temp.url
    cat part1/heada.html bg-temp.url part1/headb.html part1/core part1/tail.html > part1/index.html
    nice wkhtmltoimage --crop-w 800 --height 1080 part1/index.html part1.png
    # yori -> Taiwan 
    nice ./lai/getfeed.py
    cat /home/user/takaichi/lai/part1/head.html /home/user/takaichi/lai/part1/core /home/user/takaichi/lai/part1/tail.html > lai.html
    nice wkhtmltoimage --width 800 --crop-h 165 lai.html lai.png
    nice composite -gravity SouthWest -geometry +0+0 lai.png part1.png part1.png

    nice convert -strip -resize 800x1400! part1.png exp2.jpg

    # 26. 5. 12 
    convert -resize x360 exp2.jpg exp2-mini.jpg

    # drawing done, let's save it: 
    #cp exp2.jpg "frames/$(date -Iminutes).jpg"

    # do uploading! 

    upload_via_ftp exp1.jpg
    upload_via_ftp exp2.jpg

    ##### 

    i=$(($i+1))

    if [ -e ./last.sec ];then 
        last=$(cat ./last.sec)
    else 
        last=$(($(date "+%s")-90))
    fi

    now=$(date "+%s")
    delta=$((${now}-${last}))
    if [ $delta -gt 177 ]; then
        pillow=0
    else
        pillow=$((180-${delta}))
    fi
    echo "Last:  ${last}"
    echo "Now:   ${now}"
    echo "Delta: ${delta}"
    echo "Will sleep for ${pillow} seconds."

    sleep "${pillow}"
    date "+%s" > last.sec
done


#!/bin/sh

page=$1

curl -s "https://www.10000recipe.com/recipe/list.html?order=date&page=${page}" | pup "a[class=common_sp_link] attr{href}"


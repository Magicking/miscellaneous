#!/usr/bin/env bash
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

#
# mygal.sh - Make Your Gallery - by ubitux
#
# Usage:
#   mygal.sh <dir>          Generate new thumbnails
#   mygal.sh -r <dir>       Remove unused thumbs and generate new ones
#   mygal.sh -f <dir>       Remove all thumbs before generate ones
#
# If you don't want a file to appear in the gallery, just prefix it with '_'
#

set -e

EXT='png jpg jpeg gif'
THUMBS_DIR='.thumbs'
PAGE='index.html'
MAX_W=120
MAX_H=75

C_Black="\e[0;30m"
C_Red="\e[0;31m"
C_Green="\e[0;32m"
C_Brown="\e[0;33m"
C_Blue="\e[0;34m"
C_Purple="\e[0;35m"
C_Cyan="\e[0;36m"
C_Gray="\e[1;30m"
C_Yellow="\e[1;33m"
C_White="\e[1;37m"
C_LGray="\e[0;37m"
C_LBlue="\e[1;34m"
C_LGreen="\e[1;32m"
C_LCyan="\e[1;36m"
C_LRed="\e[1;31m"
C_LPurple="\e[1;35m"
C_Def="\e[0m"

create_page()
{
    echo -n '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
		<title>mygal.sh</title>
		<style type="text/css">
			body { background-color: #202020; color: white; font: 10px sans-serif; }
			div.p { float: left; width: '$((MAX_W+2))'px; height: '$((MAX_H+12))'px; margin: 10px; text-align: center; }
			div.f { width: 100%; overflow: hidden; }
			a img { border: 2px solid #505050; }
			a img:hover { border: 2px solid white; }
		</style>
	</head>
	<body>' > $PAGE
}

add_item()
{
    echo -n '
        <div class="p">
            <a href="'$1'"><img src=".thumbs/'$1'" alt="" /></a><div class="f">'$1'</div>
        </div>' >> $PAGE
}

write_foot()
{
    echo '
    </body>
</html>' >> $PAGE
}

get_find_string()
{
    find_str=""
    for i in $EXT
    do
        if [ "$find_str" == "" ]; then find_str="-iname \"*.$i\""
        else find_str="$find_str -or -iname \"*.$i\""; fi
    done
}

generate_thumbs()
{
    echo "[+] Generate thumbs in [$PWD]"
    create_page
    mkdir -p "$THUMBS_DIR"
    get_find_string "$EXT"
    for i in `eval "find . -maxdepth 1 $find_str | sort -f"`
    do
        f=`basename "$i"`
        if [[ "${f::1}" == "_" ]]; then
            echo -e " |--- ${C_Cyan}Ignoring [$f] (file begin with '_')${C_Def}"
            continue
        fi
        out="$THUMBS_DIR/$f"
        if [ -f "$THUMBS_DIR/$f" ]; then
            echo -e " |--- ${C_LBlue}Ignoring [$f] (thumb already exists)${C_Def}"
        else
            echo -e " |--- ${C_LGreen}Generate [$out]${C_Def}"
            convert "$f" -resize ${MAX_W}x${MAX_H} "$out"
        fi
        add_item "$f"
    done
    write_foot
}

delete_unused()
{
    echo "[+] Delete unused thumbs"
    [ ! -d "$THUMBS_DIR" ] && return
    for i in $THUMBS_DIR/*
    do
        orig_file="`basename $i`"
        if [ ! -f "$orig_file" ]
        then
            echo -e " |--- ${C_Yellow}File [$orig_file] does not exist. Remove preview [$i].$C_Def"
            rm "$THUMBS_DIR/$orig_file"
        fi
    done
}

#
# Entry point
#

if [ $# -eq 1 -a -d "$1" ]
then
    cd "$1"
    generate_thumbs "$1"
elif [ $# -eq 2 -a "$1" == "-r" -a -d "$2" ]
then
    cd "$2"
    delete_unused
    generate_thumbs "$2"
elif [ $# -eq 2 -a "$1" == "-f" -a -d "$2" ]
then
    cd "$2"
    echo '[+] Remove all thumbs'
    rm -rf .thumbs
    generate_thumbs "$2"
fi

#!/bin/bash
set -e

if [ -z "$1" ]
then
    INPUT="./accelerated-domains.china.conf"
    echo "No INPUT supplied, using default: accelerated-domains.china.conf"
else
    INPUT=$1
fi

if [ -z "$2" ]
then
    OUTPUT="./whitelist.txt"
    echo "No OUTPUT supplied, using default: whitelist.txt"
else
    OUTPUT=$2
fi

printf "! Last Modified: $(stat -L -c %y $INPUT)\n\n" > $OUTPUT
grep -e '^server' $INPUT | sed "s|^server=/\(.*\)/[^/]*$|\|\|\1|" >> $OUTPUT

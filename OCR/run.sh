#!/bin/bash

usage()
{
    echo "Usage: run.sh path/to/images/folder"
    exit
}

path_to_images=$1

if [ "$path_to_images" == "" ]; then
    usage
fi


FILES="$path_to_images/*"

for f in $FILES
do
    #echo "Processing $f file..."
    fname="$(basename -- $f)"
    fname="${fname%.jpg}"
    #echo "$fname"
    tesseract -l heb+eng $f $fname
done

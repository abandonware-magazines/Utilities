#!/bin/bash

usage()
{
    echo "Usage: extract_covers.sh path/to/pdf/folder"
    echo "PDF folder is expected to contain multiple PDFs with the standard naming convention of:"
    echo "MagazineNameN.Scanned_by_Someone.pdf"
    exit
}

path_to_pdfs=$1

if [ "$path_to_pdfs" == "" ]; then
    usage
fi

pushd $path_to_pdfs

for f in *.pdf; do
    [ -f "$f" ] || break
    echo -n $f
    if [[ ! $f =~ ^([^0-9]*)([0-9]+).*$ ]]; then
        echo " - Can't find magazine name or issue number!"
        break
    fi
    
    magazine=${BASH_REMATCH[1]}
    magazine=$(echo "$magazine" | tr '[:upper:]' '[:lower:]')

    issue=${BASH_REMATCH[2]}
    echo -n " -> $magazine, $issue"
    
    fmt_issue=`printf %d $issue`
    echo -n " -> $fmt_issue"
    
    output_path="$path_to_pdfs/output/covers/$magazine"
    
    mkdir -p $output_path
    output_file_path=$output_path/$magazine$fmt_issue.jpg

    echo ""

    gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -r144 -dFirstPage=1 -dLastPage=1 -sOutputFile=$output_file_path $f 2>&1 1>/dev/null

    if [ ! $? -eq 0 ]; then
        echo " -> Error extracting image from $f"
        break
    fi

    convert $output_file_path -verbose -resize x400\> $output_file_path;

    if [ ! $? -eq 0 ]; then
        echo " -> Error resizing image from $f"
        break
    fi
    
    echo ""
done

popd
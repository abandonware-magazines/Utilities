#!/bin/bash

usage()
{
    echo "Usage: pdf_to_images.sh path/to/pdf/folder"
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
    issue=${BASH_REMATCH[2]}
    echo -n " -> $issue"
    
    fmt_issue=`printf %03d $issue`
    echo -n " -> $fmt_issue"
    
    output_path="$path_to_pdfs/output/$magazine/$fmt_issue"
    
    mkdir -p $output_path

    gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -r144 -sOutputFile=$output_path/%02d.jpg $f 2>&1 1>/dev/null

    if [ ! $? -eq 0 ]; then
        echo " -> Error extracting images from $f"
        break
    fi
    
    echo ""
done

popd
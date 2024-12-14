#!/bin/bash

usage()
{
    echo "Usage: images_to_pdf.sh path/to/base/folder"
    echo "Base folder is expected to contain multiple subfolders with the standard naming convention of:"
    echo "MagazineNameN.Scanned_by_Someone"
    echo "Each subfolder should contain the JPEGs for the PDF"
    exit 1
}

base_path=$1

if [ "$base_path" == "" ]; then
    usage
fi

output_path="$base_path/output/PDFs"

if [[ ! -d "$base_path" ]]; then
    echo "The provided path '$base_path' is not a directory."
    exit 1
fi

mkdir -p $output_path

for subfolder in "$base_path"/*; do
    if [[ -d "$subfolder" ]]; then
        image_files=("$subfolder"/*.jpg)

        if [[ ! -e "${image_files[0]}" ]]; then
            echo "No JPEG images found in folder: $subfolder"
            continue
        fi

        output_pdf="$output_path/$(basename "$subfolder")_base.pdf"

        echo Trying to create PDF using ImageMagick
        magick -quality 95 -density 120 "${image_files[@]}" "$output_pdf"

        if [[ $? -eq 0 ]]; then
            echo "PDF created successfully: $output_pdf"

            echo Trying to optimize PDF using Ghostscript
            optimized_pdf="$output_path/$(basename "$subfolder").pdf"
            gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen \
               -dNOPAUSE -dQUIET -dBATCH -sOutputFile="$optimized_pdf" "$output_pdf"

            if [[ $? -eq 0 ]]; then
                echo "Optimized PDF created successfully: $optimized_pdf"
                rm "$output_pdf" # Remove the unoptimized PDF
            else
                echo "Failed to optimize PDF: $output_pdf"
            fi
        else
            echo "Failed to create PDF for folder: $subfolder"
        fi
    fi
done

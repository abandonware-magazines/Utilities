#!/bin/bash

usage()
{
    echo "usage: train.sh [[-c] | [-h]]"
}


clean=

while [ "$1" != "" ]; do
    case $1 in
        -c | --clean )          clean=1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

pushd tesstrain
MNAME=magazines
GT_PATH=data/$MNAME-ground-truth

if [ "$clean" = "1" ]; then
    rm -rf data/$MNAME
    rm -rf data/heb/$MNAME.*
    rm -rf $GT_PATH
fi

mkdir -p $GT_PATH
#cp ../ground_truth/* $GT_PATH
python3 ../copy_rtl_gt.py -s ../ground_truth -d $GT_PATH

make training MODEL_NAME=$MNAME LANG_TYPE=RTL PSM=7 START_MODEL=heb

make traineddata CHECKPOINT_FILES="$(ls data/$MNAME/checkpoints/*.checkpoint | head -1)" MODEL_NAME=$MNAME

sudo cp $(ls data/$MNAME/tessdata_fast/*.traineddata | head -1) /usr/share/tesseract-ocr/4.00/tessdata/heb.traineddata

popd
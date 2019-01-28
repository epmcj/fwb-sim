#!/bin/bash
set -e

IN_DIR=$1
if [ -z "$1" ]
  then
    echo "No input directory"
    exit 1
fi
OUT_DIR=$2
if [ -z "$2" ]
  then
    echo "No output directory"
    exit 1
fi
ALPHA=3
TSLOT=100
BW=$3
if [ -z "$3" ]
  then
    echo "No bandwidths available"
    exit 1
fi
FRAMES=2
COI=1

shopt -s nullglob 
for IN_FILE in "$IN_DIR"*.in;
do
    FBASE=$(basename -- "$IN_FILE")
    FBASE="${FBASE%.*}"
    SIZE="${FBASE//[^0-9]/}"
    OUT_FILE=$OUT_DIR$FBASE".out"
    echo $IN_FILE" > "$OUT_FILE
    python3 test_fwbi.py -i $IN_FILE -o $OUT_FILE -bw $BW -a $ALPHA \
            -s $TSLOT -f $FRAMES -coi $COI
done
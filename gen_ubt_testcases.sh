#!/bin/bash
# set -e

OUT_DIR=$1
if [ -z "$1" ]
  then
    echo "No output directory"
    exit 1
fi
NUM_CASES=$2
if [ -z "$2" ]
  then
    echo "No number of test cases"
    exit 1
fi
NUM_LVLS=($(seq 3 1 11)) 
MIN_DIST=2
MAX_DIST=20

for NUM_LVL in "${NUM_LVLS[@]}";
do
    OUT_FILE=$OUT_DIR"ubt_"$NUM_LVL".in"
    python3 gen_ubt_networks.py -l $NUM_LVL -d $MAX_DIST -m $MIN_DIST \
            -t $NUM_CASES -o $OUT_FILE
    echo $OUT_FILE
done

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
NUM_NODES=($(seq 100 100 1000)) 
MIN_DIST=2
MAX_DIST=20
MIN_CHILDREN=1
MAX_CHILDREN=4

for NODES in "${NUM_NODES[@]}";
do
    OUT_FILE=$OUT_DIR"rt_"$NODES".in"
    python3 gen_rt_networks.py -n $NODES -d $MAX_DIST -md $MIN_DIST \
            -c $MAX_CHILDREN -mc $MIN_CHILDREN -t $NUM_CASES -o $OUT_FILE
    echo $OUT_FILE
done

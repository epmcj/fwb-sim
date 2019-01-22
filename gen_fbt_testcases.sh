#!/bin/bash

set -e

IN_DIR=$1
OUT_DIR=$2
NUM_LVLS=($(seq 3 1 11)) 
MIN_DIST=2
MAX_DIST=20

shopt -s nullglob 
for IN_FILE in "$IN_DIR"*.in;
do
    python3 gen_fbt_tests.py [CONTINUAR]
done

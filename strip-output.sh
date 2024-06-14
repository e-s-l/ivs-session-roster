#!/bin/bash
# strip file
# assuming ran get-exp-echedules.sh > output.txt
# then run this as strip-output.sh output.txt
# to produce a plain list "exps.txt" of exp_code doy start_time duration
# (duration to be added...)

FILE=$1

NEW_FILE="exps.txt"

grep -E '[A-Za-z]{1,3}[0-9]{2,5} [0-9]{1,3} [0-9]{2}:[0-9]{2}' "$FILE" | awk '{$1=$1};1' >> $NEW_FILE

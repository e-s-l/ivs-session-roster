#!/bin/bash

#######################
# GENERATE THE ROSTER
# ie RUN THE COMPONENTS
#######################

# NEED TO CHECK INPUTS

# INPUTS
MONTH=$1

# GET THE IVS SCHEDULE FILE:
./get-exp-schedules.sh $MONTH

# GENERATE THE SPREADSHEET:
python3 vakliste_generator.py

# PULL-UP THE PRODUCE:
open test.xlsx

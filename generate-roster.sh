#!/bin/bash

#######################
# GENERATE THE ROSTER
# ie RUN THE COMPONENTS
#######################

echo "------------------------------------------------------"

# NEED TO CHECK INPUTS

# INPUTS
MONTH=$1

# GET THE IVS SCHEDULE FILE:
echo "------------------------------------------------------"
echo "Getting Experiments from IVS roster:"
./get-exp-schedules.sh $MONTH

# GENERATE THE SPREADSHEET:
echo "------------------------------------------------------"
echo "Generating Roster and Spreadsheet:"
python3 vakliste_generator.py

# PULL-UP THE PRODUCE:
echo "------------------------------------------------------"
echo "Opening Spreadsheet:"
open test.xlsx

#
echo "------------------------------------------------------"
echo "------------------------------------------------------"

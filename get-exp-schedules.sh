#!/bin/bash

#######################################
# FUNCTIONS:

get_file() {
	# to download the master or intensive file from the cddis database
	#
	local FILE="$1"  # $MASTER_FILE
	local URL="$2"	 # https://cddis.nasa.gov/archive/vlbi/ivscontrol/master$YR.txt
	if ! [ -f "$FILE" ]
	then
		echo "(Getting $FILE schedule file...)"
		if ! curl --location --cookie cookies.txt "$2" > "$1"
		then
			echo "Failed to download $FILE from $URL"
			exit 1
		fi
		echo "------------------------------------------------------"
	fi

}

get_exp_info() {
	# to get the relevant information from the line
	#
	local line="$1"
	#the line structure and what we wish to capture (using "()") from it:
	local regex=".*\|([A-Za-z]{1,3}[0-9]{2,5}).*\|(\s{0,2}[0-9]{1,3})\|([0-9]{2}:[0-9]{2}).*\|(\s{0,2}[0-9]{0,2}:[0-9]{2}).*\|([A-Za-z]+.*[A-Za-z])\s.*"	 # ok but can't distinguish cancelled exps. hack fix below...

	if [[ $line =~ $regex ]]
	then
		EXP_CODE="${BASH_REMATCH[1]}"
		EXP_DOY="${BASH_REMATCH[2]}"
		EXP_START_TIME="${BASH_REMATCH[3]}"
		EXP_DUR="${BASH_REMATCH[4]}"
		EXP_STATIONS="${BASH_REMATCH[5]}"
	fi
}

process_file() {
	# to parse and process the experiment roster file we just downloaded
	#
	local EXP_COUNT=0
	local NNNS_EXP_COUNT=0
	local EXPS_THIS_WEEK=()
	local FILE="$1"
	local OUTPUT_FILE="$2"

	# Read the input text file line by line and parse each line
	while read -r line
	do
		if ! [[ $(echo $line | grep "\\---") ]]
		then
			#
			get_exp_info "$line"
			#
			if [[ "$EXP_DOY" -ge "$DOY" ]] && [[ "$EXP_DOY" -le "$DOY_END" ]]
			then
				(( EXP_COUNT++ ))
				if [[ $(echo "$EXP_STATIONS" | grep -) ]]
				then
					EXP_STATIONS=$(echo $"$EXP_STATIONS" | cut -d ' ' -f1)	 #this deletes the cancelled exps from the string
				fi
				#
				if [[ $(echo "$EXP_STATIONS" | grep Nn) ]] || [[ $(echo "$EXP_STATIONS" | grep Ns) ]] || [[ $(echo "$EXP_STATIONS" | grep NnNs) ]]
				then
					EXP_TELE=""
					EXP_TELE+=$(echo "$EXP_STATIONS" | grep -o Nn)
					EXP_TELE+=$(echo "$EXP_STATIONS" | grep -o Ns)
					#
					EXP_INFO="$EXP_CODE $EXP_TELE $EXP_DOY $EXP_START_TIME $EXP_DUR"
					EXPS_THIS_WEEK+=("$EXP_INFO")
					(( NNNS_EXP_COUNT++ ))
				fi
			fi
		fi
	done < $FILE

	echo "------------------------------------------------------"
	echo "	There are $EXP_COUNT experiments.         "
	if [[ "$NNNS_EXP_COUNT" -gt 0 ]]
	then
		echo "	NN and/or Ns is in $NNNS_EXP_COUNT:"
		for EXP in "${EXPS_THIS_WEEK[@]}"
		do
			echo "		$EXP"
			echo "$EXP" >> $OUTPUT_FILE
		done
	fi
	echo "------------------------------------------------------"
}

#######################################
# SET-UP
set -e
# Input is month to generate roster for...
MONTH=$1
#MONTH="June"
# Assuming the present year...
YR=$(date +%Y)
#
#MONTH_NUM=$(date -d "$MONTH 1" +%m)
#
MY_STR_1="${MONTH} 1, ${YR}"
DOY=$(date -d "$MY_STR_1" +%j)			# adjust this to be a range for a gien month?
#

LAST_DAY=$(date -d "$MY_STR_1 + 1 month - 1 day" +%d)
#
MY_STR_2="${MONTH} ${LAST_DAY}, ${YR}"
DOY_END=$(date -d "$MY_STR_2" +%j)
#
OUTPUT_FILE="experiments_nn_ns.txt"
> $OUTPUT_FILE
######################################
echo "------------------------------------------------------"
echo "	Considering days $DOY - $DOY_END of ${YR}..."
echo "------------------------------------------------------"
#######################################
### GET 24-HOUR SESSIONS MASTER FILE:
FILE="master${YR}.txt"
get_file "$FILE" "https://cddis.nasa.gov/archive/vlbi/ivscontrol/master$YR.txt"
echo "            --- MASTER ---"
process_file "$FILE" "$OUTPUT_FILE"
######################################
### GET 1-HOUR INTENSIVE SESSIONS FILE:
INTENSIVES_FILE="intensives${YR}.txt"
get_file "$INTENSIVES_FILE" "https://cddis.nasa.gov/archive/vlbi/ivscontrol/master$YR-int.txt"
echo "            --- INTENSIVES ---"
process_file "$INTENSIVES_FILE" "$OUTPUT_FILE"
######################################


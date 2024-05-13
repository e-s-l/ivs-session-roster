#!/bin/bash

#######################################
# FUNCTIONS:

get_file() {
	# to download the master or intensive file from the cddis database
	local FILE="$1"  # $MASTER_FILE
	local URL="$2"	 # https://cddis.nasa.gov/archive/vlbi/ivscontrol/master$YR.txt

	if ! [ -f "$FILE" ]
	then
		echo "(Getting $FILE schedule file...)"
		if ! curl --location --cookie cookies.txt "$1" > "$2"
		then
			echo "Failed to download $FILE from $URL"
			exit 1
		fi
	fi
}

get_exp_info() {
	local line="$1"
	#the line structure and what we wish to capture (using "()") from it:
	local regex=".*\|([A-Za-z]{1,3}[0-9]{2,5}).*\|(\s{0,2}[0-9]{1,3})\|([0-9]{2}:[0-9]{2}).*\|([A-Za-z]+.*[A-Za-z])\s.*"	 # ok but can't distinguish cancelled exps.

	if [[ $line =~ $regex ]]
	then
		EXP_CODE="${BASH_REMATCH[1]}"
		EXP_DOY="${BASH_REMATCH[2]}"
		EXP_START_TIME="${BASH_REMATCH[3]}"
		EXP_STATIONS="${BASH_REMATCH[4]}"
	fi
}

process_file() {
	#to parse and process the experiment roster file we just downloaded
	local EXP_COUNT=0
	local NN_EXP_COUNT=0
	local NN_EXPS_THIS_WEEK=()
	local NS_EXP_COUNT=0
	local NS_EXPS_THIS_WEEK=()
	local FILE="$1"

	# Read the input text file line by line and parse each line
	while read -r line
	do
		if ! [[ $(echo $line | grep "\\---") ]]
		then
			#
			get_exp_info "$line"
			#
			if [[ "$EXP_DOY" -ge "$DOY" ]] && [[ "$EXP_DOY" -le "$DOYp7" ]]
			then
				(( EXP_COUNT++ ))
				if [[ $(echo "$EXP_STATIONS" | grep -) ]]
				then
					EXP_STATIONS=$(echo $"$EXP_STATIONS" | cut -d ' ' -f1)	 #this deletes the cancelled exps from the string
				fi
				if [[ $(echo "$EXP_STATIONS" | grep Nn) ]]
				then
					(( NN_EXP_COUNT++ ))
					EXP_INFO="$EXP_CODE $EXP_DOY $EXP_START_TIME"
					NN_EXPS_THIS_WEEK+=("$EXP_INFO")
				fi
				if [[ $(echo "$EXP_STATIONS" | grep Ns) ]]
				then
					(( NS_EXP_COUNT++ ))
					EXP_INFO="$EXP_CODE $EXP_DOY $EXP_START_TIME"
					NS_EXPS_THIS_WEEK+=("$EXP_INFO")
				fi
			fi
		fi
	done < $FILE


	echo "------------------------------------------------------"
	echo "	There are $EXP_COUNT experiments.         "
	if [[ "$NN_EXP_COUNT" -gt 0 ]]
	then
		echo "	NN is in $NN_EXP_COUNT:"
		for EXP in "${NN_EXPS_THIS_WEEK[@]}"
		do
			echo "		$EXP"
		done
	fi
	if [[ "$NS_EXP_COUNT" -gt 0 ]]
	then
		echo "	NS is in $NS_EXP_COUNT:"
		for EXP in "${NS_EXPS_THIS_WEEK[@]}"
		do
			echo "		$EXP"
		done
	fi
	echo "------------------------------------------------------"



}

#######################################
# SET-UP
DOY=$(date +%j)
YR=$(date +%Y)
DOYp7=$(date -d +"7 days" +%j)
######################################
echo "------------------------------------------------------"
echo "------------------------------------------------------"
echo "	Today is Day $DOY of $YR."
echo "	This week (days $DOY - $DOYp7)..."
echo "------------------------------------------------------"
#######################################
### GET 24-HOUR SESSIONS MASTER FILE:
FILE="master${YR}.txt"
get_file "$FILE" "https://cddis.nasa.gov/archive/vlbi/ivscontrol/master$YR.txt"
echo "            --- MASTER ---"
process_file "$FILE"
######################################
### GET 1-HOUR INTENSIVE SESSIONS FILE:
INTENSIVES_FILE="intensives${YR}.txt"
get_file "$INTENSIVES_FILE" "https://cddis.nasa.gov/archive/vlbi/ivscontrol/master$YR-int.txt"
echo "            --- INTENSIVES ---"
process_file "$INTENSIVES_FILE"
######################################
echo "------------------------------------------------------"
######################################


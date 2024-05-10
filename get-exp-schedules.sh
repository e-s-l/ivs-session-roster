#!/bin/bash

# SET-UP
DOY=$(date +%j)
YR=$(date +%Y)
DOYp7=$(date -d +"7 days" +%j)

#######################################

### GET 24-HOUR SESSIONS MASTER FILE:
MASTER_FILE="master${YR}.txt"

if ! [ -f "$MASTER_FILE" ]
then
   	echo "(Getting master schedule...)"
    	curl --location --cookie cookies.txt "https://cddis.nasa.gov/archive/vlbi/ivscontrol/master$YR.txt" > $MASTER_FILE
fi

######################################

EXP_COUNT=0
NN_EXP_COUNT=0
NN_EXPS_THIS_WEEK=()
NS_EXP_COUNT=0
NS_EXPS_THIS_WEEK=()

# Read the input text file line by line and parse each line
while read -r line
do
	regex=".*\|([A-Za-z]{1,2}[0-9]{3,5}).*\|(\s{0,2}[0-9]{1,3})\|.*\|([A-Za-z]+.*[A-Za-z])\s.*" 
	if [[ $line =~ $regex ]]
	then
		EXP_CODE="${BASH_REMATCH[1]}"
		EXP_DOY="${BASH_REMATCH[2]}"
		EXP_STATIONS="${BASH_REMATCH[3]}"
	fi
	
		
	if [[ "$EXP_DOY" -gt "$DOY" ]] && [[ "$EXP_DOY" -lt "$DOYp7" ]]
	then
		(( EXP_COUNT++ ))
		
		if [[ $(echo $"$EXP_STATIONS" | grep Nn) ]] 
		then
			(( NN_EXP_COUNT++ ))
			NN_EXPS_THIS_WEEK+=("$EXP_CODE")
		fi
		if [[ $(echo $"$EXP_STATIONS" | grep Ns) ]] 
		then
			(( NS_EXP_COUNT++ ))
			NS_EXPS_THIS_WEEK+=("$EXP_CODE")
		fi
	fi

done < $MASTER_FILE

#######################################

echo "------------------------------------------------------"
echo "            Today is Day $DOY of $YR."
echo "------------------------------------------------------"
echo "This week (days $DOY - $DOYp7) there are ${EXP_COUNT} experiment(s)."
echo "------------------------------------------------------"
echo "    And..."
echo "            NN is in ${NN_EXP_COUNT}: ${NN_EXPS_THIS_WEEK[*]}."
echo "            NS is in ${NS_EXP_COUNT}: ${NS_EXPS_THIS_WEEK[*]}."
echo "------------------------------------------------------"

######################################


#!/bin/bash

# CONTROL

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

### GET 1-HOUR INTENSIVE SESSIONS FILE:
INTENSIVES_FILE="intensives${YR}.txt"
if ! [ -f "$INTENSIVES_FILE" ]
then
   	echo "(Getting intensives schedule...)"
    	curl --location --cookie cookies.txt "https://cddis.nasa.gov/archive/vlbi/ivscontrol/master$YR-int.txt" > $INTENSIVES_FILE
fi

######################################

MASTER_COUNT=0
INTENSIVE_COUNT=0
NN_EXP_COUNT=0
NN_EXPS_THIS_WEEK=()
NS_EXP_COUNT=0
NS_EXPS_THIS_WEEK=()

#the line structure and what we wish to capture (using "()") from it:
regex=".*\|([A-Za-z]{1,3}[0-9]{2,5}).*\|(\s{0,2}[0-9]{1,3})\|([0-9]{2}:[0-9]{2}).*\|([A-Za-z]+.*[A-Za-z])\s.*"	 # ok but can't distinguish cancelled exps.
#regex=".*\|([A-Za-z]{1,3}[0-9]{2,5}).*\|(\s{0,2}[0-9]{1,3})\|([0-9]{2}:[0-9]{2}).*\|([A-Za-z]+.*[A-Za-z])\s+\|.*"	# not any better

# Read the input text file line by line and parse each line
while read -r line
do
	if ! [[ $(echo $line | grep "\\---") ]]
	then
		if [[ $line =~ $regex ]]
		then
			EXP_CODE="${BASH_REMATCH[1]}"
			EXP_DOY="${BASH_REMATCH[2]}"
			EXP_START_TIME="${BASH_REMATCH[3]}"
			EXP_STATIONS="${BASH_REMATCH[4]}"
		fi
		if [[ "$EXP_DOY" -gt "$DOY" ]] && [[ "$EXP_DOY" -lt "$DOYp7" ]]
		then
			(( MASTER_COUNT++ ))
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
done < $MASTER_FILE

# now check the INTENSIVES_FILE, and append to the list of experiments for each antenna

while read -r line
do
	if ! [[ $(echo $line | grep "\\---") ]]
	then
		if [[ $line =~ $regex ]]
		then
			EXP_CODE="${BASH_REMATCH[1]}"
			EXP_DOY="${BASH_REMATCH[2]}"
			EXP_START_TIME="${BASH_REMATCH[3]}"
			EXP_STATIONS="${BASH_REMATCH[4]}"
		fi
		if [[ "$EXP_DOY" -gt "$DOY" ]] && [[ "$EXP_DOY" -lt "$DOYp7" ]]
		then
			(( INTENSIVE_COUNT++ ))

			if [[ $(echo "$EXP_STATIONS" | grep -) ]]
			then
				EXP_STATIONS=$(echo $"$EXP_STATIONS" | cut -d ' ' -f1)	 #this deletes the cancelled exps from the string
			fi

			if [[ $(echo "$EXP_STATIONS" | grep Nn) ]]
			then
				(( NN_EXP_COUNT++ ))
				EXP_INFO="$EXP_CODE $EXP_DOY $EXP_START_TIME (1-hr)"
				NN_EXPS_THIS_WEEK+=("$EXP_INFO")
			fi
			if [[ $(echo "$EXP_STATIONS" | grep Ns) ]]
			then
				(( NS_EXP_COUNT++ ))
				EXP_INFO="$EXP_CODE $EXP_DOY $EXP_START_TIME (1-hr)"
				NS_EXPS_THIS_WEEK+=("$EXP_INFO")
			fi
		fi
	fi
done < $INTENSIVES_FILE



#######################################

echo "------------------------------------------------------"
echo "            Today is Day $DOY of $YR."
echo "------------------------------------------------------"
echo "This week (days $DOY - $DOYp7) there are ${MASTER_COUNT} 24-hr and ${INTENSIVE_COUNT} 1-hr experiment(s)."
echo "------------------------------------------------------"
echo "And..."
echo "            NN is in ${NN_EXP_COUNT}:"
echo
for EXP in "${NN_EXPS_THIS_WEEK[@]}"
do
	echo "		$EXP"
done
echo
echo "            NS is in ${NS_EXP_COUNT}:"
echo
for EXP in "${NS_EXPS_THIS_WEEK[@]}"
do
	echo "		$EXP"
done
#echo "		(CODE|DOY|UTC)"
echo
echo "------------------------------------------------------"

######################################


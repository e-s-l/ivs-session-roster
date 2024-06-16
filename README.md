# ABOUT:

## vakliste_generator.py

  - Create lists of objects representing experiments, and on-duty observers.
  - Make a schedule associating the two lists.
  - Generate a spreadsheet to present the roster.

## get-exp-schedules.sh & strip-output.sh

  - Silly little script to get the roster for the up-coming week's IVS experiments.
  - Good practice in regex, but not really that practical...
  - It works but is slow and the whole approach feels wrong, very hacked together... will return to this another time, refreshed...
  - Should use awk and ditch the while loop.
  - Properly figure out the regex so don't need grep to catch the cancelled session or the
    blank lines.... another time 



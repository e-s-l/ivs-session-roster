# Generate Roster

Given a list of experiments scheduled by the IVS & a list of observers, this code produces a spreadsheet with each experiment assigned an on-duty obserser.

[TOC]

## Operations


First, download the IVS roster text files as `masterYEAR.txt` & `intensivesYEAR.text` where `YEAR` is <i>e.g.</i> 2024.

The script `get-exp-schedules.sh` will download these for you, but first you need to log-in & download a `cookies.txt` file for the site, so that curl can access it. Otherwise just end up with the html for a log-in page. So it's probably easier just to download & save with the correct names...

Then run `generate-roster.sh Month` where `Month` is the <i>e.g.</i>  July (capitalised, spelled correctly... still need to implement an input parser to catch issues with this).

This will run:
- `get-experiment-schedules.sh` which will process these text files, finding the experiments for our observatory for the given month, & put these into a single text file called `experiments_nn_ns.txt`
- `vakliste_generator.py` which will produce the spreadsheet, named simply (at this stage) `test.xlsx`
- Finally it will open the spreadsheet, please definitely check it!

## Info.

The main scripts are the following.

### vakliste_generator.py

- Create lists of objects representing experiments & on-duty observers.
- Make a schedule associating the two lists.
- Generate a spreadsheet to present the roster.

### get-exp-schedules.sh & strip-output.sh

- Silly little script to get the roster for the up-coming week's IVS experiments.
- Good practice in regex, but not really that practical...
- It works but is slow & the whole approach feels wrong, very hacked together... will return to this another time, refreshed..
- Should use awk & ditch the while loop.
- Properly figure out the regex so don't need grep to catch the cancelled session or the blank lines.... another time

## Other

### Drafts/

Ignore.

## TODO

- Catch user inputs and other basic error tests...
- Consider any edge-cases in the 'plotting' that could be implemented in this automisation..



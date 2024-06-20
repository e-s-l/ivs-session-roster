# Generate Roster

Given a list of experiments scheduled by the IVS & a list of observers, this code produces a spreadsheet with each experiment assigned an on-duty observer.

#### Table of Contents

1. [Operations](#Operations)
2. [Information](#Info.)
3. [Other](#Other)

**************************************************************

## Operations

In an ideal world, one would just run `generate-roster.sh Month` where `Month` is the <i>e.g.</i>  April. But as it stands, out of the box, this won't work.

So, first, download the IVS roster text files as `masterYEAR.txt` & `intensivesYEAR.text` where `YEAR` is *e.g.* 2024. The problem here is that to access these text files you must log in. So the script `get-exp-schedules.sh` can and will download these for you, but first you need to log-in & download a `cookies.txt` file for the site, so that curl can access it. (I used a firefox extension to get this cookies file.) Otherwise, you just end up with the html for a log-in page. So it's probably easier just to download & save with the correct names, at least at first... or until I figure out how to fix this.

Then, second, run `generate-roster.sh Month` where `Month` is the *e.g.*  July (capitalised, spelled correctly... I still need to implement an input parser to catch issues with this). This very basic shell script will run:

- `get-experiment-schedules.sh` which will process these text files, finding the experiments for our observatory for the given month, & put these into a single text file called `experiments_nn_ns.txt`. This output file is the input into the next script...
- Also inputted into the next script is a file containing any & all observers. This file needs to be similarly formatted, as one observer name per line.
- `vakliste_generator.py` which will produce the spreadsheet, named simply (at this stage) `test.xlsx`.
- Finally, it will open the spreadsheet for you to see, please definitely check it!

So, to summarise:

For this to work, the user, you, need to log in to the IVS website and download a cookies file *or* download the schedule files. If the later, then name with the forms given above. These files are the input into `get-exp-schedules.sh` which processes these & produces another text file. This file, as well as another file with the observer list, is then read by  `generate-roster.sh` which finally produces the spreadsheet. (But `generate-roster.sh` is really `vakliste_generator.py`. And this also requires the class declarations `observers.py` & `session.py`.)

**************************************************************

## Info.

The main script `generate-roster.sh` is a simple wrapper to three actual scripts. These are the following.

### vakliste_generator.py

Simply this uses the python openxl library to create a basic spreadsheet. But first there are a few steps:

- Create lists of objects representing experiments & on-duty observers.
- Make a schedule associating the two lists.
- Then finally generate a spreadsheet to present the roster.

### get-exp-schedules.sh

This was the actual start & goal of this little project, which then with a weekend's leisure, balloned to include the above. But in brief:

- This is a silly little script to get the roster for the up-coming week's IVS experiments. I considered just good practice in regex, but not really that practical...
- It works but is slow & the whole approach feels wrong, very hacked together... will return to this another time, refreshed.. For example, should use awk & ditch the while loop.
- I also still need to properly figure out the regex such that we don't need grep to catch the cancelled session or the blank lines... another time.

**************************************************************

## Other

### Drafts/

Ignore this directory please. It's just old stuff I didn't have the heart to delete.

### TODO

Lots of things to do... But just to name a few (in loose order of priority):

- Catch user inputs and other basic error tests.
- Consider any edge-cases in the 'plotting' that could be implemented in this automisation.
- Clean up the code text, and decide on better names for the files created, *etc. etc.*



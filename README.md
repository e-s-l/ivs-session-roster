<h1>Generate Roster</h1>

<p> Given a list of experiments scheduled by the IVS, and a list of observers, produce a spreadsheet with each experiment assigned an on-duty obserser.</p>

<h2>Operations:</h2>

<p>First, download the IVS roster text files as <samp>masterYEAR.txt</samp> and <samp>intensivesYEAR.text</samp> where YEAR is <i>e.g.</i> 2024 </p>
<p>The script get-exp-schedules.sh will download these for you, but first you need to log-in and download a <samp>cookies.txt</samp> file for the site, so that curl can access it. Otherwise just end up with the html for a log-in page. So it's probably easier just to download and save with the correct names...</p>
<p>Then run <samp>generate-roster.sh Month</samp> where Month is the <i>e.g.</i>  July (capitalised, spelled correctly... still need to implement an input parser to catch issues with this).</p>
<p>This will run:</p>
<ul>
  <li><samp>get-experiment-schedules.sh</samp> which will process these text files into a single text file called <samp>experiments_nn_ns.txt</samp></li>
  <li><samp>vakliste_generator.py</samp> which will produce the spreadsheet, named simply (at this stage) <samp> test.xlsx </samp></li>
  <li>Finally it will open the spreadsheet, please definitely check it!</li>
</ul>

<h2>Info:</h2>

<h3>vakliste_generator.py</h3>

<ul>
  <li>Create lists of objects representing experiments, and on-duty observers.</li>
  <li>Make a schedule associating the two lists.</li>
  <li>Generate a spreadsheet to present the roster.</li>
  <li></li>
</ul>

<h3>get-exp-schedules.sh & strip-output.sh</h3>

<ul>
  <li>Silly little script to get the roster for the up-coming week's IVS experiments.</li>
  <li>Good practice in regex, but not really that practical...</li>
  <li>It works but is slow and the whole approach feels wrong, very hacked together... will return to this another time, refreshed...</li>
  <li>Should use awk and ditch the while loop.</li>
  <li>Properly figure out the regex so don't need grep to catch the cancelled session or the blank lines.... another time </li>
  <li></li>
</ul>

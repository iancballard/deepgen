# deepgen
Task for distinguishing low and high levels of visual concept learning

Installation instructions

Instructions for Mac OSX
Open up a terminal window
Install xcode tools
xcode-select --install
Create a conda environment
Download and install anaconda
conda create -n deepgen python==3.7
conda activate deepgen
Install necessary packages
pip install psychopy
pip install seaborn
To run the experiment
Open terminal
conda activate deepgen
cd {EXPERIMENT_FOLDER}/ 
python task.py {MODE} -s {SUBJECT} -r {RUN_NUMBER}
There are 4 possible modes
“practice”
Loads detailed instructions and 15 practice trials
“experimenter”
Runs the experiment, but with short intertrial and interstimulus intervals (so you can get a sense of the expt. without waiting around for the fMRI timing)
“fmri”
Version for the scanner. When each run begins, the subject indicates when they are ready to begin by pressing “1”. Then it will wait for the experimenter to press “space” to begin. This way, the experimenter can start the scanner and the experiment at the same time
“behavior”
Same as fMRI but without 12s pause at the beginning and end of the experiment. It does not wait for the “space” key to begin, so a subject can cycle through all of the runs on their own, and take breaks between runs as needed. Suitable for piloting the fMRI study outside of the scanner.

Useful things to know about the experiment
12 runs of 25 trials each (300 trials total)
Each fmri run is 458 seconds long (7.5 minutes)
6 blocks the algorithm rewards what IT thinks is most similar, 6 blocks it rewards what V2 thinks is most similar. The subject does not know which is which. Reward probabilities for choosing in accordance with the algorithm are .85. So, if it is a V2 block and the block probability is .75, if the subject chooses what V2 thinks is the most similar option, then the subject has a 75% of reward, whereas if the subject selects the other option, the subject has a 25% of reward. 
Which block is first is random (see below for details on randomization), the subject will do 6 blocks of IT or V2, then 6 blocks of the second (V2 or IT). 
One block is chosen at random to count for real, and each reward is added up with the conversion rate of 1 reward equals $.50, and added to the subject payment as a bonus. Too slow responses are deducted from the total. 

Useful things to know about the software
The software checks periodically for “escape” and will close if it detects this key. If you want to stop the experiment, simply press “esc” (you may have to wait a few seconds for the next time in the trial the software checks)
The software will sequentially cycle through all runs. However, if you need to redo a run (for example, if the scanner doesn’t start correctly), you can change the {RUN_NUMBER} flag and it will start from there (and keep going sequentially through the runs). So, for example, say you start with run number 1 and later need to stop in the middle of run 5. To start again, simple type python task.py {MODE} -s {SUBJECT} -r 5 and it will keep going from there
The software saves the data at the end of each run. If you stop in the middle of a run, no data will be saved.
The software does not overwrite saved data. If it detects that a file already exists with the intended filename, it will append a “+” 
Block order, trial order, and block reward probabilities are all randomized. This randomization is linked to the subject id {SUBJECT}. So, every time you run the same subject, the same randomized designs will load (which is useful if you have to stop and restart the experiment), but any change to that subject label will cause a completely new randomization (so be careful not to change this for the same subject!)
At startup, the script checks the refresh rate of the screen against the expected refresh rate. If it’s too far off, the experiment will exit before starting and issue a warning. If it’s just off by a little (maybe .5 HZ), then just take note and restart the script. If it’s happening a lot, try turning off demanding computer tasks (disconnecting from the Internet is a good first step). If it deviates by a lot (i.e., the screen is actually 30 HZ), this will create problems with the experiment timing. You can turn off this behavior with the “test_refresh” flag in the params.py script.
Some details on the scripts
Params.py
The majority of the parameters controlling experiment behavior
Task.py
This actually runs through all the trials of the task, updating the screen and recording keypresses and saving data
Datastruct.py
This handles a variety of housekeeping tasks at startup, including loading the timing files and implementing randomization 

The data are saved as .pkl files that are somewhat difficult to access. To make things easier, I included an “extract_data.py” script that extracts and compiles the data
First, include subjects that you care about in the “subjects.txt” file
Then, run “python extract_data.py” from inside the experiment folder
The script will
Print warnings if it detects duplicate data for a specific subject and run number (check those out, likely you only want one of the two)
Prints bonuses to be paid for each subject
Saves an aggregate dataframe as ‘/data/data.csv’, which can be analyzed with any program that can handle csv files


import os
from pickle import TRUE
dir = os.getcwd()
stimulus_path = dir + "/wordlist.csv"

#import ppc
import psychopy
from psychopy import visual, core, event, gui
from random import sample
import random
import pandas as pd
import numpy as np
from random import randint
import glob
import csv
import re

#POPUP box
popup = gui.Dlg(title = "Demonstrative Choice Task")
popup.addField("Participant ID:")
popup.addField("Gender", choices = ["Male","Female","Other"])
popup.addField("Age:")
popup.show()
if popup.OK:
    ID = popup.data[0]    
    gender = popup.data[1]
    age = popup.data[2]
else:
    core.quit()

#Define window
#win = visual.Window(fullscr=True, color='black')
win = visual.Window((1000,800), color='black')

#Define stopwatch
stopwatch=core.Clock()

#Create logfile 
columns = ['ID', 'Age', 'Gender', 'trial','word','choice','response','rt', 'choice_order','stim_onset','block']
index =  np.arange(0) # array of numbers for the number of samples
logfile = pd.DataFrame(columns=columns, index=index)

#Define stimuli 
words = pd.read_csv(stimulus_path, sep=",",header=None)
stimuli = [w for w in words.iloc[:,1]]
random.shuffle(stimuli)

practice_stimuli = ['cow','water','box','airplane','drawing','mountain']
random.shuffle(practice_stimuli)

def show_info(txt):
# show a message
    msg = visual.TextStim(win, text=txt, pos = [0,0.2], height = 0.05)
    msg.draw()
    win.flip()
# wait for a keypress
    key = event.waitKeys()
    if key == ['q']:
        core.quit()
        win.close()

def show_info2(txt):
# show a message
    msg = visual.TextStim(win, text=txt, pos = [0,0.2], height = 0.05)
    msg.draw()
    win.flip()

def show_fixation():
# show a message
    msg = visual.TextStim(win, text="+", pos = [0,0], height = 0.1)
    msg.draw()
    win.flip()
# wait for a keypress
    core.wait(6)

def choices_option():
    rand_ind = random.randint(0,1)
    if rand_ind==0: 
        choices = "this            that"
    if rand_ind==1:
        choices = "that            this"
    return choices, rand_ind

def prac_trial(k, choices):
    show_fixation()
    
    word = practice_stimuli[k]
    msg = visual.TextStim(win, text=word, pos=[0,0], height=0.09)
    msg2 = visual.TextStim(win, text=choices, pos=[0,-0.4], height = 0.07)
    msg.draw()
    msg2.draw()
    win.flip()
    
    key = event.waitKeys()
    if key == ['q']:
        core.quit()
        win.close()
    

def trial(k, choices, rand_ind, block, first):
    log = pd.DataFrame(columns=['ID', 'Age', 'Gender', 'trial','word','choice','response','rt', 'choice_order', 'stim_onset','block'], index=np.arange(0))
    #show_fixation()
    if k==first: 
        show_fixation()

    word = stimuli[k]
    msg = visual.TextStim(win, text=word, pos=[0,0], height=0.2)
    msg2 = visual.TextStim(win, text=choices, pos=[0,-0.3], height = 0.1)
    msg.draw()
    msg2.draw()
    win.flip()
    
    stimOnset = stopwatch.getTime()
    core.wait(1)

    msg = visual.TextStim(win, text="+", pos = [0,0], height = 0.1)
    msg2 = visual.TextStim(win, text=choices, pos=[0,-0.3], height = 0.1)
    msg.draw()
    msg2.draw()
    win.flip()
# wait for a keypress
    core.wait(5, hogCPUperiod=5)    
    key = event.getKeys(keyList=['b','y','q'], timeStamped=stopwatch)
    
    if len(key)==0: 
        rt=0.0
        key = [['NA']]
        response='NA'
    else:
        rt=key[0][1]-stimOnset

        if key[0][0] == 'q':
            win.close() 
            core.quit()
        
        if key[0][0]=='b':
            if rand_ind==0: 
                response = 'this'
            else:
                response = 'that'
        else: 
            if rand_ind==0: 
                response='that'
            else: 
                response='this'


    log = log.append({
        'ID': ID,
        'Age': age,
        'Gender': gender,
        'trial': k,
        'word': word,
        'choice':response,
        'rt':rt,
        'choice_order':rand_ind,
        'response':key[0][0],
        'stim_onset':stimOnset,
        'block':block
    }, ignore_index=True)
    return(log)

#Run test 
filename = ID +'.csv'
#output_file = os.path.join(path, filename)
logfile.to_csv(filename, index=False) 

show_info("Thank you for participating in our short survey on lexical choice in demonstrative reference. \nIn what follows, you will be presented with a series of 120 words, and asked to match them with either 'this' or 'that'. \nThere is no specific rule to follow: just make your choice based on your first and immediate preference. \nUse the left and right button to indicate your choice. \nNotice that the position of 'this' and 'that' response buttons changes randomly.")

#Block 1 
show_info2("Please wait for the experiment to start.")
event.waitKeys(keyList=['q','t'])
stopwatch.reset()

#trials_total = len(stimuli)
trials_total = 15
trials_block = 5

for k in range(0,trials_block):
    choices, rand_ind = choices_option()    
    logfile = logfile.append(trial(k,choices, rand_ind, block=1, first=0))
    logfile.to_csv(filename, index=False)

show_info("Great job! \nYou have now completed the first block of the experiment \nTake a break and wait for instructions from the experimenter.")

#Block 2 
show_info2("Please wait for the experiment to start.")
event.waitKeys(keyList=['q','t'])
stopwatch.reset()
for k in range(trials_block,trials_block*2):
    choices, rand_ind = choices_option()    
    logfile = logfile.append(trial(k,choices, rand_ind, block=2, first=trials_block))
    logfile.to_csv(filename, index=False)

show_info("Great job! \nYou have now completed the second block of the experiment \nTake a break and wait for instructions from the experimenter.")

#Blcok 3
show_info2("Please wait for the experiment to start.")
event.waitKeys(keyList=['q','t'])
stopwatch.reset()
for k in range(trials_block*2,trials_total):
    choices, rand_ind = choices_option()    
    logfile = logfile.append(trial(k,choices, rand_ind, block=3, first=trials_block*2))
    logfile.to_csv(filename, index=False)

show_info("Well done \nYou have now completed the experiment \nPlease wait for instructions from the experimenter.")

win.close()
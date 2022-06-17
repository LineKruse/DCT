#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 08:27:39 2022

@author: au553087
"""

import os
from pickle import TRUE
dir = os.getcwd()
stimulus_path = dir + "/wordlist_clusters.csv"

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
popup.show()
if popup.OK:
    ID = popup.data[0]    
else:
    core.quit()

#Define window
#win = visual.Window(fullscr=True, color='black')
win = visual.Window((1000,800), color='black')

#Define stopwatch
stopwatch=core.Clock()

#Create logfile 
columns = ['ID','trial','word','choice','response','rt', 'choice_order','stim_onset','block']
index =  np.arange(0) # array of numbers for the number of samples
logfile = pd.DataFrame(columns=columns, index=index)


practice_stimuli = ['cow','water','box','airplane','drawing','mountain','whale','baby','screw','phone','coffee','building','note','idea','bus']
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
    log = pd.DataFrame(columns=['ID','trial','word','choice','response','rt', 'choice_order', 'stim_onset','block'], index=np.arange(0))
    #show_fixation()
    if k==first: 
        show_fixation()

    word = practice_stimuli[k]
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
        
        if key[0][0]=='left':
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
filename = ID +'_pracTrials.csv'
#output_file = os.path.join(path, filename)
logfile.to_csv(filename, index=False) 

show_info("This is a practice round. \nYou will be presented with one noun at a time. Match each word with either 'this' or 'that'. \nUse the left and right arrows to make your choice. \nPress a key to start the practice.")

#Block 1 
# show_info2("Please wait for the experiment to start.")
# event.waitKeys(keyList=['q','t'])
# stopwatch.reset()

trials = len(practice_stimuli)
#trials_total = 15
# trials_block = 5

for k in range(0,trials):
    choices, rand_ind = choices_option()    
    logfile = logfile.append(trial(k,choices, rand_ind, block=1, first=0))
    logfile.to_csv(filename, index=False)

show_info("Well done. \nThe practice round is completed.")

# #Block 2 
# show_info2("Please wait for the experiment to start.")
# event.waitKeys(keyList=['q','t'])
# stopwatch.reset()
# for k in range(trials_block,trials_block*2):
#     choices, rand_ind = choices_option()    
#     logfile = logfile.append(trial(k,choices, rand_ind, block=2, first=trials_block))
#     logfile.to_csv(filename, index=False)

# show_info("Great job! \nYou have now completed the second block of the experiment \nTake a break and wait for instructions from the experimenter.")

# #Blcok 3
# show_info2("Please wait for the experiment to start.")
# event.waitKeys(keyList=['q','t'])
# stopwatch.reset()
# for k in range(trials_block*2,trials_total):
#     choices, rand_ind = choices_option()    
#     logfile = logfile.append(trial(k,choices, rand_ind, block=3, first=trials_block*2))
#     logfile.to_csv(filename, index=False)

# show_info("Well done \nYou have now completed the experiment \nPlease wait for instructions from the experimenter.")

win.close()
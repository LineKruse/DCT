import os
from pickle import TRUE
dir = os.getcwd()
stimulus_path = dir + "/pseudorandomized_stimuli_list.csv"

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
#win = visual.Window((1000,800), color='black')
win = visual.Window(fullscr=True, color='black')

#Define stopwatch
stopwatch=core.Clock()

#Create logfile 
columns = ['ID', 'Age', 'Gender', 'trial','word','choice','response','rt', 'choice_order','stim_onset','block']
index =  np.arange(0) # array of numbers for the number of samples
logfile = pd.DataFrame(columns=columns, index=index)

#Load stimuli 
words = pd.read_csv(stimulus_path, sep=",")
words = [w for w in words.loc[:,'word']]
# stimuli = [w for w in words.iloc[:,1]]
# random.shuffle(stimuli)

#Find 10 words at random to be repeated (differs for each participant)
random10 = random.choices(words, k=10)

#Find index in word list of placeholders (rep1, rep2, rep3, etc.)
reps = [words.index(l) for l in words if l.startswith('rep')]

#Replace placeholders with the 10 words to be repeated 
words[reps[0]] = random10[0]
words[reps[1]] = random10[1]
words[reps[2]] = random10[2]
words[reps[3]] = random10[3]
words[reps[4]] = random10[4]
words[reps[5]] = random10[5]
words[reps[6]] = random10[6]
words[reps[7]] = random10[7]
words[reps[8]] = random10[8]
words[reps[9]] = random10[9]

stimuli = words


#Add the random 10 rep words to list (placeholders: "rep1", "rep2", "rep3", etc.)

#Define stimuli 
# words = pd.read_csv(stimulus_path, sep=",")

# words.columns = ['word','groups']
# c1 = [w for w in words.loc[words['groups'] == 1, 'word']]
# c2 = [w for w in words.loc[words['groups'] == 2, 'word']]
# c3 = [w for w in words.loc[words['groups'] == 3, 'word']]
# c4 = [w for w in words.loc[words['groups'] == 4, 'word']]
# c5 = [w for w in words.loc[words['groups'] == 5, 'word']]
# c6 = [w for w in words.loc[words['groups'] == 6, 'word']]
# c7 = [w for w in words.loc[words['groups'] == 7, 'word']]
# c8 = [w for w in words.loc[words['groups'] == 8, 'word']]
# c9 = [w for w in words.loc[words['groups'] == 9, 'word']]
# c10 = [w for w in words.loc[words['groups'] == 10, 'word']]
# c11 = [w for w in words.loc[words['groups'] == 11, 'word']]
# c12 = [w for w in words.loc[words['groups'] == 12, 'word']]
# c13 = [w for w in words.loc[words['groups'] == 13, 'word']]
# c14 = [w for w in words.loc[words['groups'] == 14, 'word']]
# c15 = [w for w in words.loc[words['groups'] == 15, 'word']]
# c16 = ['rep1','rep2','rep3','rep4','rep5','rep6','rep7','rep8','rep9','rep10']
# c1.append('depression')
# c8.append('woman')
# c8.append('man')

# lists = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16]

# # # seq = []
# # # for i in range(0,15): 
# # #     seq.append([i]*len(lists[i]))
# # # seq1 = [x for xs in seq for x in xs]

# group_order = [1,0,3,9,11,7,8,6,12,14,13,2,5,10,4,1,0,3,9,11,7,8,6,12,14,13,2,5,10,15,4,1,0,3,9,11,
# 7,8,6,12,14,13,2,5,10,4,1,0,3,9,11,7,8,6,12,14,13,2,5,15,10,4,1,0,3,9,11,7,8,6,12,14,13,2,5,10,4,1,
# 0,3,9,11,7,8,0,6,12,14,13,15,2,5,10,4,1,0,3,9,11,7,8,6,12,14,13,2,5,10,1,0,3,9,11,7,8,6,12,14,13,15,2,5,
# 10,1,0,3,9,11,7,8,6,12,14,13,2,5,10,1,0,3,9,11,7,8,6,12,14,13,2,15,5,10,1,0,3,9,11,7,8,6,12,14,13,
# 2,5,1,0,3,9,11,7,8,6,12,14,13,2,1,0,15,3,9,11,7,8,6,12,14,13,2,1,0,3,9,11,7,8,6,12,14,13,1,0,3,9,
# 11,7,8,6,15,12,14,1,0,3,9,11,7,8,6,1,0,3,9,11,7,8,6,1,0,3,9,11,7,8,1,0,3,9,15,11,7,1,0,3,9,11,7,1,0,
# 3,9,11,7,1,0,3,9,11,1,0,3,9,11,1,0,3,7,9,15,11,1,0,3,9,11,1,0,3,9,1,0,3,9,1,0,3,9,1,7,0,3,1,0,3,1,0,3,
# 1,0,15,1,1]

# #Sample words randomly from the groups according to the group order 
# word_list = []
# for num in group_order: 
#     g = lists[num]
#     word = random.choice(g)
#     word_list.append(word)
#     lists[num].remove(word)


#dict = {'sem_group': group_order, 'word': word_list}  
       
#df = pd.DataFrame(dict) 
    
# #saving the dataframe 
#df.to_csv(stimulus_path)


#practice_stimuli = ['cow','water','box','airplane','drawing','mountain']
#random.shuffle(practice_stimuli)

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

# def prac_trial(k, choices):
#     show_fixation()
    
#     word = practice_stimuli[k]
#     msg = visual.TextStim(win, text=word, pos=[0,0], height=0.09)
#     msg2 = visual.TextStim(win, text=choices, pos=[0,-0.4], height = 0.07)
#     msg.draw()
#     msg2.draw()
#     win.flip()
    
#     key = event.waitKeys()
#     if key == ['q']:
#         core.quit()
#         win.close()
    

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
path = 'data/'
output_file = os.path.join(path, filename)
logfile.to_csv(output_file, index=False) 

show_info("Thank you for participating in our short survey on lexical choice in demonstrative reference. \nIn what follows, you will be presented with a series of words, and asked to match them with either 'this' or 'that'. \nThere is no specific rule to follow: just make your choice based on your first and immediate preference. \nUse the left and right button to indicate your choice. \nNotice that the position of 'this' and 'that' response buttons changes randomly.")

#Block 1 
show_info2("Please wait for the experiment to start.")
event.waitKeys(keyList=['q','t'])
stopwatch.reset()

trials_total = len(stimuli)
trials_block = int(trials_total/3)
#trials_total = 15
#trials_block = 5

for k in range(0,trials_block):
    choices, rand_ind = choices_option()    
    logfile = logfile.append(trial(k,choices, rand_ind, block=1, first=0))
    logfile.to_csv(output_file, index=False)

show_info("Great job! \nYou have now completed the first block of the experiment \nTake a break and wait for instructions from the experimenter.")

#Block 2 
event.waitKeys(keyList=['q','z'])
show_info2("Please wait for the experiment to start.")
event.waitKeys(keyList=['q','t'])
stopwatch.reset()
for k in range(trials_block,trials_block*2):
    choices, rand_ind = choices_option()    
    logfile = logfile.append(trial(k,choices, rand_ind, block=2, first=trials_block))
    logfile.to_csv(output_file, index=False)

show_info("Great job! \nYou have now completed the second block of the experiment \nTake a break and wait for instructions from the experimenter.")

#Blcok 3
event.waitKeys(keyList=['q','z'])
show_info2("Please wait for the experiment to start.")
event.waitKeys(keyList=['q','t'])
stopwatch.reset()
for k in range(trials_block*2,trials_total):
    choices, rand_ind = choices_option()    
    logfile = logfile.append(trial(k,choices, rand_ind, block=3, first=trials_block*2))
    logfile.to_csv(output_file, index=False)

show_info("Well done \nYou have now completed the experiment \nPlease wait for instructions from the experimenter.")

win.close()
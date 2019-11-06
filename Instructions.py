# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 14:25:46 2019

@author: Jacopo
"""

import time, numpy as np
from psychopy import visual as vis, event, core

#win = vis.Window(fullscr = True, allowGUI = True, winType = 'pyglet', color = 'gray', monitor = 'Latitude_Jacopo', units = 'deg', gammaErrorPolicy = 'ignore') #monitor = 'Benq_xl2411'

space = 'Press a button to continue..'

test1 = 'Respond correctly to these targets to continue!'

message_1_welcome = 'Welcome to the experiment, {0}! In this visual search task, you are asked to detect as quickly \
and accurately as possible a target among distractors.\n\nThe items are shapes of 3 different random colors (red, blue or green)\
 with a gap on one side:\n\n\t- Target items have a gap on either the upper or the lower part.\
\n\t- Distractors have a gap on the left or on the right.\n\nPlease look at the fixation point in the center of the screen and start your search from there!'

message_2_target = 'The target will be always present and you have to respond to its orientation: \
\n\n- Press the button on the top with your {1} index finger if the gap is on the top of the shape.\
\n- Press the button on the bottom with your {2} index finger if the gap is on the bottom of the shape.'

message_3_cues = 'Before the search, a set of 3 colored cues will be appear. Please note that: \
\n\n- Only ONE of the 3 cues will have the same color of the target, helping you in the visual search!\
\n\n- The other 2 cues will be colored randomly.'

message_objective = '**You have to guess which of the three cues is the one that is OFTEN colored as the target in order to make a quick detection of the target!**'

message_4_switch = 'The only cue often colored as the target will change sometimes:\
\n\n- After each break (end of the block)\
\n- A few times within each block (but note that it won\'t change too often - NOT every few trials...'

message_5_questions = 'Please ask any question now if something is not clear!\
\n\nYou will start with some practice trials as soon as you press a button..'



objmessage = vis.TextStim(win, text = message_objective,\
                        color='black',\
                        wrapWidth = 32.5,\
                        height = 1,\
                        pos=(0,-5),\
                        alignVert = 'center')


spacetext = vis.TextStim(win, text = space,\
                        color='white',\
                        wrapWidth = 32.5,\
                        height = .5,\
                        pos=(0,-8.5),\
                        alignVert = 'bottom')

testtext = vis.TextStim(win, text = test1,\
                        color='white',\
                        wrapWidth = 32.5,\
                        height = .8,\
                        pos=(0,-7.5),\
                        alignVert = 'bottom')

textbox_1 = vis.TextStim(win, text = message_1_welcome.format('participant'),\
                        color='black',\
                        wrapWidth = 32.5,\
                        height = .9,\
                        pos=(0,0),\
                        alignVert = 'center')

textbox_2 = vis.TextStim(win, text = message_2_target,\
                        color='black',\
                        wrapWidth = 32.5,\
                        height = .9,\
                        pos=(0,2),\
                        alignVert = 'bottom')

textbox_3 = vis.TextStim(win, text = message_3_cues,\
                        color='black',\
                        wrapWidth = 32.5,\
                        height = .9,\
                        pos=(0,5),\
                        alignVert = 'center')

textbox_4 = vis.TextStim(win, text = message_4_switch,\
                        color='black',\
                        wrapWidth = 32.5,\
                        height = .9,\
                        pos=(0,0),\
                        alignVert = 'center')

textbox_5 = vis.TextStim(win, text = message_5_questions,\
                        color='black', bold = True,\
                        wrapWidth = 30.5,\
                        height = 1.2,\
                        pos=(0,0),\
                        alignVert = 'center')



  
mex = [message_1_welcome,message_2_target,message_3_cues,message_objective]

keyboard = True
while True:
    a = event.getKeys()
    if not a == ['left'] and len(a) != 0:
        break
    if a == ['left']:
        print('want to go back')
    spacetext.draw()
    textbox_1.draw()
    win.flip()

event.clearEvents()
while True:
    a = event.getKeys()
    if not a == ['left'] and len(a) != 0:
        break
    if a == ['left']:
        print('want to go back')
    testtext.draw()
    textbox_2.draw()
    win.flip()

event.clearEvents()

while True:
    a = event.getKeys()
    if not a == ['left'] and len(a) != 0:

        break
    if a == ['left']:
        print('want to go back')
    spacetext.draw()
    textbox_3.draw()
    objmessage.draw()
    win.flip()
    
while True:
    a = event.getKeys()
    if not a == ['left'] and len(a) != 0:

        break
    if a == ['left']:
        print('want to go back')
    spacetext.draw()
    textbox_4.draw()
    win.flip()
    
while True:
    a = event.getKeys()
    if not a == ['left'] and len(a) != 0:
        quit
        win.close()
        core.quit()
        break
    if a == ['left']:
        print('want to go back')
    textbox_5.draw()
    win.flip()
#for i in np.repeat(5,5):
#    textbox_1.draw()
#    win.flip()
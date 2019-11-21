# -*- coding: utf-8 -*-
"""
Created on Wed Oct 2 15:11:32 2019

@author: Jacopo

Experimental procedure script for the visual search task - explicit mode. Data is imported from a dataframe and the response is saved in a txt"""


####IMPROVE THE SCRIPT######
#Put all messages in a seprate script and import all the messages + translation.
#Response functions and the response in the instructions should be better defined and divided.
#device can probably be set only in the response function...right?
#the GUI appears too often and should work better
#smooth transaction b/w practice and real experiment??
#implicit or explicit mode should be in one script only with the possibility to choose from GUI
#Feedback on mistakes and on misses?
#
#
#
#
#############################

import time, random, warnings, numpy as np, pandas as pd

print('Executing Cshape script for implicit mode!\n\n')
time.sleep(2)

from psychopy import visual as vis, core



#Import useful variables from init script
from Init_Cshape import headers, colors, headers_answer, trials_total,\
 color_labels, number_positions, keyboard, color_space,\
time_search, KeyResp, quiT, ms_to_frames, row_save, mon, esc_keys,allowed_keys,file_name,\
dataframe_name, PN, part_name, mode, hand, age, gender, practice, dutch,\
wrong_key_text, late_answer_text,end_practice, bye_text,\
neg_feedback_text, break_time, row_crash, crash, fix_max, fix_min,\
iti_max,iti_min, Q0_text, Q1_text, Q2_0_text, wrong_answer_text,\
keys_4_answ, keys_4_answ_reduced, Q1_0_text, Q2_text, questions_text

from Cshape_functions_implicit import Response, Instructions, breaK, TrueColors, WrongAnswer


# Set boolean for practice or not.
#if mode == 'Practice':
#    practice = True
#else:
#    practice = False

# Save data file if we are not in practice mode. Will be updated at the end with the total time.
if not practice and not crash:
    info_file = open('data\\part_n_' + PN + '\\info_' + PN +'.txt', 'x')
    info_file.write('file_name = ' + file_name + '\n' +\
                    'dataframe_name = ' + dataframe_name + '\n' +\
                    'Participant number = ' + PN + '\n' +\
                    'hand = ' + hand + '\n' +\
                    'age = ' + age + '\n' +\
                    'gender = ' + gender + '\n')
    info_file.close()


counterbalance = True if int(PN) % 2 == 0 else False  #True when participant number is even




if not keyboard:
    import pyxid2 as pyxid
else:
    from psychopy import event


# Set a name for the file with GUI func



##############################
##     IMPORT DATAFRAME     ##
##############################

df = pd.read_csv(filepath_or_buffer = dataframe_name, header = 0, names = ['Index']+headers, engine = 'python')

##Transform dataframes values so that they are meaningful for psychopy
# Define functions
ori_func_targ = lambda x: 90 if x == 0 else 270  # 90 has gap in the bottom, gap is up when ori is 270
ori_func_distr = lambda x: 180 if x == 1 else x

color_func = lambda x: color_labels[0] if x == 0 else (color_labels[1] if x == 1 else color_labels[2])


if keyboard:
    cor_resp_func = lambda x: 'down' if x == 0 else 'up'
    df.loc[:,'correct_response'] = df.correct_response.apply(cor_resp_func)
#else:
#    cor_resp_func = lambda x: KeyResp[0] if x ==  else KeyResp[1]
#    df.loc[:,'correct_response'] = df.correct_response.apply(cor_resp_func)

#define function for translating colors for draw search array
#color_C_per_position_func = lambda x: color_labels[0] if x < number_positions/len(colors) else (color_labels[2] if x >= number_positions-(number_positions/len(colors)) else color_labels[1])
    

color_C_per_position_func = lambda x: color_labels[0] if x < number_positions/len(colors) else (color_labels[2] if x >= number_positions-(number_positions/len(colors)) else color_labels[1])

# Apply functions

#df.loc[:,'color_target'] = df.loc[:,'color_target'].apply(color_func)

df.loc[:,'ori_target'] = df.ori_target.apply(ori_func_targ)

for col1 in df.loc[:,'ori_distractor_0':'ori_distractor_11']:
    df.loc[:,col1] = df.loc[:,col1].apply(ori_func_distr)


# Initialize some variables to save in the txt

# Reaction times
RTs_cedrus = np.repeat(-1.,trials_total)
RTs_keyboard = np.repeat(-1.,trials_total)

real_target_location = np.repeat(-1,trials_total)

# Just check the timings of the different windows flipped.
trial_time = np.repeat(-1.,trials_total)
items_time = np.repeat(-1.,trials_total)
placeholder_time = np.repeat(-1.,trials_total)
cue_time = np.repeat(-1.,trials_total)

# Response variables
if keyboard:
    response_key = ['nope']*trials_total # Which key was pressed

else:
    response_key = np.repeat(-1.,trials_total) # Which key was pressed
is_response_right = np.repeat(-1.,trials_total) # Is it the right response?
button_pressed = np.repeat(-1.,trials_total) # ONLY for Cedrus, how long the button has been pressed?

guessed_cues = np.repeat(-1.,trials_total)
Key4cues = ['1','2','3']


########################
##     CEDRUS BOX     ##
########################

if not keyboard:

    pyxid.use_response_pad_timer = True
    
    device = pyxid.get_xid_devices()[0]
    
    time.sleep(1)
    
else:
    device = None

########################
##     PARAMETERS     ##
########################

# Set parameters for search items' features

sizeItem = 1.5

# Set parameters for real positions

PS = 12/5.3 #divide each quadrant in 3 equal parts

# Adjust the y and x of the items close to the axis
mod = 1.32
positionReal = [(PS/mod,3*PS),(2*PS,2*PS),(3*PS,PS/mod),(3*PS,-PS/mod),(2*PS,-2*PS),(PS/mod,-3*PS),
    (-PS/mod,-3*PS),(-2*PS,-2*PS),(-3*PS,-PS/mod),(-3*PS,PS/mod),(-2*PS,2*PS),(-PS/mod,3*PS)] # Define all 12 positions of the search array, these will be the pos attribute of the search items


# Set parameters for cues

r = .4
size_c = 1


d = 3
f = -2

triangle_side = 4

yT = ((triangle_side**2-(triangle_side/2)**2)**(1/2))/2
xT = triangle_side/2

pos0 = (-xT,-yT)
pos1 = (0,yT)
pos2 = (xT,-yT)


# Placeholder parameters

w = 1.4
h1 = 1.4
size_p = 1
lineW = 3.5


# Fixation cross vertices

a = .05 # x-axis top-right edge
#b = .05 # y-axis top-right edge
c = .2 + a # 'lenght' of one part of the cross
FixVert = ((a,-c),(a,-a),(c,-a),(c,a),(a,a),(a,c),(-a,c),(-a,a),(-c,a),(-c,-a),(-a,-a),(-a,-c))


# Set coordinates of the vertices and the gap for the C shape (search item)

x,y = (.6,.6)
g,h = (.3,.3)
gap = .2


# If gap == 0 then the shape is a square without one side. This is just a note not important for execution.

if gap < 0 or gap > g:
    raise Exception('set a proper gap value for the polygon: gap should be between 0 and %s'%g)




######################################
##     VISUAL PART AND STIMULI      ##
######################################



if 'test' in mon.name:
    warnings.warn('Using Test monitor!!')

# Make sure we are using gamma calibration if monitor is Benq
if 'Jacop' not in mon.name and 'test' not in mon.name:
    if mon.gammaIsDefault():
        raise Exception ('Monitor is not using gamma!!')

# Create the window
gray = (0,0,.5) if color_space == 'hsv' else ((0,0,0,) if color_space == 'rgb' else 'gray')
win = vis.Window(fullscr = True, winType = 'pyglet', color = gray, monitor = mon, units = 'deg', gammaErrorPolicy = 'ignore', colorSpace = color_space) #monitor = 'Benq_xl2411'
win.allowGUI = False
win.mouseVisible = False
# Define the 12 polygon vertices
CVert = ((x,h-gap),(x,y),(-x,y),(-x,-y),(x,-y),(x,(-h+gap)),(g,(-h+gap)), (g,-h), (-g,-h), (-g,h), (g,h), (g,h-gap))

#Define C shape
C = vis.ShapeStim(win, vertices = CVert, fillColor = [0,0,0], lineWidth = 0, size = sizeItem, pos = (0,0), ori = 25, fillColorSpace = color_space)

C_prot = vis.ShapeStim(win, vertices = CVert, fillColor = [0,0,0], lineWidth = 0, size = sizeItem, pos = (0,0), ori = 25, fillColorSpace = color_space)


#C_arrstim = vis.ElementArrayStim(win, nElements= 12, sizes = sizeItem, sfs=3, xys=xys, colors=[180, 1, 1])

# Define Placeholders
Place_Holder0 = vis.Rect(win, width = w, height = h1, size = size_p, lineWidth = lineW, lineColor = 'black', pos = pos0)
Place_Holder1 = vis.Rect(win, width = w, height = h1, size = size_p, lineWidth = lineW, lineColor = 'black', pos = pos1)
Place_Holder2 = vis.Rect(win, width = w, height = h1, size = size_p, lineWidth = lineW, lineColor = 'black', pos = pos2)

# Define cues
C0 = vis.Circle(win, size = size_c, radius = r, lineWidth = 0,fillColor = [0,0,0], fillColorSpace = color_space, pos = pos0)
C1 = vis.Circle(win, size = size_c, radius = r, lineWidth = 0,fillColor = [0,0,0], fillColorSpace = color_space, pos = pos1)
C2 = vis.Circle(win, size = size_c, radius = r, lineWidth = 0,fillColor = [0,0,0], fillColorSpace = color_space, pos = pos2)

cue_prot = vis.Circle(win, size = size_c, radius = r, lineWidth = 0, fillColor = 'black')

move_right = 4
move_down = 3

cue_prot0 = vis.Circle(win, size = 1.2, radius = r, lineWidth = 0, fillColor = 'green', pos = (pos0[0] - move_right,pos0[1] - move_down))
cue_prot1 = vis.Circle(win, size = 1.2, radius = r, lineWidth = 0, fillColor = 'red', pos = (pos1[0] - move_right, pos1[1] - move_down))
cue_prot2 = vis.Circle(win, size = 1.2, radius = r, lineWidth = 0, fillColor = 'blue', pos = (pos2[0] - move_right,pos2[1] - move_down))


# Fixation cross
fixation = vis.ShapeStim(win, vertices = FixVert, fillColor = 'black', lineWidth = 0, size = 1, pos = (0,0))


# Feedback messages
wrong_key = vis.TextStim(win, text = wrong_key_text, height = .6, pos = (0,0), color = 'red', bold = True)

late_answ = vis.TextStim(win, text = late_answer_text, height = .6, pos = (0,0), color = 'red', bold = True)


end_practice_message = vis.TextStim(win, text = end_practice,\
                    color='black', bold = False,\
                    wrapWidth = 32,\
                    height = 1,\
                    pos=(0,0),\
                    alignVert = 'center')


neg_feedback = vis.TextStim(win, text = neg_feedback_text , height = .6, pos = (0,0), color = 'crimson', bold = True, wrapWidth = 30)
pos_feedback = vis.TextStim(win, text = 'Default', height = .6, pos = (0,0), color = 'green', bold = True, wrapWidth = 30)


if practice:
    limits = np.array([750,950,1650,2100,3000])  # For pos feedback during pratice
    if keyboard:
        limits = limits / 1000  # For pos feedback during pratice

############################
##     INSTRUCTIONS       ##
############################

#Function from Chshape_functions
Instructions(part_number=int(PN), part_name=part_name, win = win, item = C_prot, mode = mode,\
             device = device, KeyResp = KeyResp, ori_targ = [90,270], keyboard = keyboard, quiT = quiT,\
             allowed_keys = allowed_keys, clock_items = None, esc_keys = esc_keys, dutch = dutch) 

core.wait(1)


breaks = []
break_row = []

####################################
##     EXPERIMENTAL PROCEDURE     ##
####################################

# Initialize some clocks to check the timings and to get reaction times


total_clock = core.Clock()
clock_placeholder = core.Clock()
clock_cues = core.Clock()
clock_items = core.Clock()
clock_trial = core.Clock()
break_clock = core.Clock()
break_clock.reset(break_time * 60)

if not keyboard:
    device.reset_base_timer() #should be called just before first trial



# Repeat for the number of trials
for rowI in range(row_crash,trials_total):

# Set cue identity

    cue_identity_temp = df.loc[rowI,'cue_identity_def']
    cue_validity_temp = df.loc[rowI,'cue_validity_def']
    
#    # Breaks - count the cue switches and do a break every 3 cue switch
#    if rowI != trials_total-1 and rowI != 0:
#        if df.loc[rowI,'cue_identity_def'] != df.loc[rowI-1, 'cue_identity_def']:
#            cue_switch_counter += 1

    # Make a break after how many switch?
    if not practice and break_clock.getTime() > 0:
        rest_clock = core.Clock()
        breaK(win,device, keyboard, quiT, allowed_keys, clock_items, row = rowI+1, response = is_response_right,\
              rt = RTs_keyboard if keyboard else RTs_cedrus, dutch = dutch,\
              crash = crash, row_start = row_crash)
        breaks.append(rest_clock.getTime())
        break_row.append(rowI)
        break_clock.reset(break_time * 60)


# Randomize positions for search items

    start_position = df.loc[rowI, 'Start_position']
    positionIndexTrue = np.arange(start_position, start_position + number_positions, dtype = 'int')
    positionIndexTrue[positionIndexTrue >= number_positions] -= number_positions


# Randomize stimuli orientation

    positionTarget = df.loc[rowI,'position_target']
    ori_vector = df.loc[rowI,'ori_distractor_0':'ori_distractor_11']
    ori_target = df.loc[rowI,'ori_target']

    real_target_location[rowI] = positionIndexTrue[int(positionTarget)]


# Set cue and target colors

    color_target = df.loc[rowI,'color_target']


    true_colors = TrueColors(target_position = positionTarget,\
                             target_color = color_target,\
                             colors = colors)

    # Just the text for the hint



#####################
##     DRAWING     ##
#####################
    

    clock_trial.reset()


    #This should present the stimuli for 30-54 frames (corresponds to 500-900 ms)
#    for frame in time_placeholder:
#        fixation.draw()
#        if hints and rowI < 20:
#            Hint.draw()
#        if not hints:
#            Place_Holder0.draw()
#            Place_Holder1.draw()
#            Place_Holder2.draw()
#        if hints and rowI <= 11:
#            Place_Holder0.draw()
#        if hints and rowI > 11 and rowI < 20:
#            Place_Holder1.draw()
#        if hints and rowI >= 20:
#            Place_Holder0.draw()
#            Place_Holder1.draw()
#            Place_Holder2.draw()
#
#
#        win.flip()
#

    # Wait random time
#    rnd = random.randrange(500,901)/1000
#    core.wait(rnd)

#    clock_cues.reset()
#
#    for frame in time_cues:
#
#        fixation.draw()
#        if hints and rowI < 20:
#            Hint.draw()
#        if not hints:
#            Place_Holder0.draw()
#            Place_Holder1.draw()
#            Place_Holder2.draw()
#        if hints and rowI <= 11:
#            Place_Holder0.draw()
#        if hints and rowI > 11 and rowI < 20:
#            Place_Holder1.draw()
#        if hints and rowI >= 20:
#            Place_Holder0.draw()
#            Place_Holder1.draw()
#            Place_Holder2.draw()
#        
#        C0.draw()
#        C1.draw()
#        C2.draw()
#        
#        win.flip()
#
#    cue_time[rowI] = clock_cues.getTime()

#    core.wait(2)

    for frame in range(random.randrange(ms_to_frames(fix_min),ms_to_frames(fix_max), ms_to_frames(100))):

        fixation.draw()
#        if hints:
#            Hint2.draw()

        win.flip()

    # Wait random time
#    rnd = random.randrange(1000,1300)
#    core.wait(rnd)


    # Search array draw. Draw 12 times the Cshape, with varying positions, colors and orientations.
    
#    fixation.draw()
#    if hints:
#        Hint2.draw()

    # Draw search array:

    for indexP, repI in zip(positionIndexTrue, range(len(positionIndexTrue))):


        C.fillColor = color_func(true_colors[0]) if repI <= 3 else (color_func(true_colors[2]) if repI > 7 else color_func(true_colors[1]))
        C.pos = positionReal[indexP]

        C.ori = ori_vector[repI]
        if repI == positionTarget:
            C.ori = ori_target

        C.draw()

    fixation.draw()


    if keyboard:
        event.clearEvents()

    win.flip()
    clock_items.reset()



######################
##     RESPONSE     ##
######################


    Press_key, Time_key, ReleaseResponse = Response(device = device, keyboard = keyboard, quiT = quiT,\
                                                          time_search = time_search, allowed_keys = allowed_keys,\
                                                          clock_items = clock_items, row = rowI)

    # Keep track of elapsed time just for check
    items_time[rowI] = clock_items.getTime()
    trial_time[rowI] = clock_trial.getTime()

    if Press_key is not None:
        if not keyboard:

            RTs_cedrus[rowI] = Time_key
            button_pressed[rowI] = ReleaseResponse['time'] - Time_key
        else:
            RTs_keyboard[rowI] = round(Time_key,4)

        response_key[rowI] = Press_key

#        print(Press_key, Time_key, sep ='     ')

        if Press_key == df['correct_response'][rowI]:
            is_response_right[rowI] = 1
            if practice:
                if Time_key > limits[4]:
                    pos_feedback.text = 'Right! But you can be faster than this!' if not dutch else 'Correct! Maar je kunt sneller zijn dan dit!'
                if Time_key <= limits[4] and Time_key > limits[3]:
                    pos_feedback.text = 'Right! But you won\'t have all this time in the real experiment!'if not dutch else 'Correct! Maar je zal niet zoveel tijd hebben in het echte experiment!'
                if Time_key <= limits[3] and Time_key > limits[2]:
                    pos_feedback.text = 'Right! Pretty quick..can you go faster?' if not dutch else 'Correct! Redelijk snel...kun je nog sneller reageren?'
                if Time_key <= limits[2] and Time_key > limits[1]:
                    pos_feedback.text = 'Right! Nice reaction time..try to lower it even further!' if not dutch else 'Correct! Goede reactietijd...probeer nog sneller te reageren!'
                if Time_key <= limits[1] and Time_key > limits[0]:
                    pos_feedback.color = 'lawnGreen'
                    pos_feedback.text = 'Right! Very fast!' if not dutch else 'Correct! Heel snel!'
                if Time_key <= limits[0]:
                    pos_feedback.color = 'lime'
                    pos_feedback.text = 'Right! Impressively fast!!!' if not dutch else 'Correct! Indrukwekkend snel!!'
                pos_feedback.draw()
                pos_feedback.color = 'green'
                win.flip()
                time.sleep(3)

        elif Press_key not in KeyResp:
            if quiT and Press_key in esc_keys:
                print('QUIT! Key %s'%Press_key)
                win.close()
                core.quit()

            else:
                is_response_right[rowI] = -2 #Pressed a wrong button
                for frame in range(150):
                    wrong_key.draw()
                    win.flip()

        else:
            is_response_right[rowI] = 0
            if practice:
                neg_feedback.draw()
                win.flip()
                time.sleep(4)


    else:        # No answer!
        #Should warn participant to answer more quickly
        is_response_right[rowI] = -1
        
        for frame in range(120):
            late_answ.draw()
            win.flip()
#    if practice and df.loc[rowI,'valid_trial'] == 0:
#        invalid_message.draw()
#        win.flip()
#        time.sleep(9)

    # Inter-trial interval (with fixation cross?)
    for frame in range(random.randrange(ms_to_frames(iti_min),ms_to_frames(iti_max), ms_to_frames(100))):
        fixation.draw()
#        if not hints:
#            Place_Holder0.draw()
#            Place_Holder1.draw()
#            Place_Holder2.draw()
#        if hints and rowI <= 11:
#            Place_Holder0.draw()
#        if hints and rowI > 11 and rowI < 20:
#            Place_Holder1.draw()
#        if hints and rowI >= 20:
#            Place_Holder0.draw()
#            Place_Holder1.draw()
#            Place_Holder2.draw()

        win.flip()



    if rowI == trials_total-1:
        if not practice: #End of practice
            end_practice_message.draw()
            win.flip()
            time.sleep(3)
        else:  # End of real experiment - question time  THIS CAN BE ALL CONDENSED IN ONE STIMULUS AND JUST CHANGE THE TEXT
            bye = vis.TextStim(win, text = bye_text,\
                    color='black', bold = True,\
                    wrapWidth = 32,\
                    height = 1,\
                    pos=(0,0),\
                    alignVert = 'center')
            question_time = vis.TextStim(win, text = questions_text,\
                              color='black', bold = False,\
                              wrapWidth = 32,\
                              height = 1,\
                              pos=(0,0),\
                              alignVert = 'center')

            Q0 = vis.TextStim(win, text = Q0_text,\
                    color='black', bold = False,\
                    wrapWidth = 32,\
                    height = 1,\
                    pos=(0,0),\
                    alignVert = 'center')
            Q1 = vis.TextStim(win, text = Q1_text,\
                    color='black', bold = False,\
                    wrapWidth = 32,\
                    height = 1,\
                    pos=(0,0),\
                    alignVert = 'center')
            Q1_0 = vis.TextStim(win, text = Q1_0_text,\
                    color='black', bold = False,\
                    wrapWidth = 32,\
                    height = 1,\
                    pos=(0,0),\
                    alignVert = 'center')
            Q2 = vis.TextStim(win, text = Q2_text,\
                    color='black', bold = False,\
                    wrapWidth = 32,\
                    height = 1,\
                    pos=(0,0),\
                    alignVert = 'center')
            Q2_0 = vis.TextStim(win, text = Q2_0_text,\
                    color='black', bold = False,\
                    wrapWidth = 32,\
                    height = 1,\
                    pos=(0,0),\
                    alignVert = 'center')
            
            wrong_answer = vis.TextStim(win, text = wrong_answer_text, height = .8, pos = (0,-5), color = 'red', bold = True)

            question_time.draw()
            win.flip()
            Response(device = device, keyboard = keyboard, quiT = quiT,\
                                          time_search = 9000, allowed_keys = None,\
                                          clock_items = clock_trial, row = rowI)

            #Did you notice any regularities regarding the color of the target?
            #Please press the top bottom for ‘yes’ and the bottom button for ‘no’
            Q0.draw()
            win.flip()
            A0 = Response(device = device, keyboard = keyboard, quiT = quiT,\
                                                      time_search = 9000, allowed_keys = None,\
                                                      clock_items = clock_trial, row = rowI)[0]

            if A0 not in keys_4_answ_reduced:
                A0 = WrongAnswer(keyboard = keyboard, question = Q0, answer = A0,\
                                 warning = wrong_answer, win = win, device = device, quiT = quiT,\
                                 rowI = rowI, keyss = keys_4_answ_reduced)



            #Was the target often colored with one specific color throughout the whole experiment?
            #Please press the top bottom for ‘yes’ and the bottom button for ‘no
            Q1.draw()
            win.flip()
            A1 = Response(device = device, keyboard = keyboard, quiT = quiT,\
                                                      time_search = 9000, allowed_keys = None,\
                                                      clock_items = clock_trial, row = rowI)[0]

            if A1 not in keys_4_answ_reduced:
                A1 = WrongAnswer(keyboard = keyboard, question = Q1, answer = A1,\
                                 warning = wrong_answer, win = win, device = device, quiT = quiT,\
                                 rowI = rowI, keyss = keys_4_answ_reduced)
            A1_0 = None
            if (keyboard and A1 == '1') or (A1 == 0 and not keyboard) : #Response on keyboard or cedrus is yes
                Q1_0.draw() #'Which color do you think the target was most often colored with?
                win.flip()
                A1_0 = Response(device = device, keyboard = keyboard, quiT = quiT,\
                                                          time_search = 9000, allowed_keys = None,\
                                                          clock_items = clock_trial, row = rowI)[0]
    
                if A1_0 not in keys_4_answ:
                    A1_0 = WrongAnswer(keyboard = keyboard, question = Q1_0, answer = A1_0,\
                                     warning = wrong_answer, win = win, device = device, quiT = quiT,\
                                     rowI = rowI, keyss = keys_4_answ)

            Q2.draw() # 'Did you notice that the most probable color of the target was changing during the experiment?
            win.flip()
            A2 = Response(device = device, keyboard = keyboard, quiT = quiT,\
                                                      time_search = 9000, allowed_keys = None,\
                                                      clock_items = clock_trial, row = rowI)[0]

            if A2 not in keys_4_answ_reduced:
                A2 = WrongAnswer(keyboard = keyboard, question = Q2, answer = A2,\
                                 warning = wrong_answer, win = win, device = device, quiT = quiT,\
                                 rowI = rowI, keyss = keys_4_answ_reduced)

            A2_0 = None
            if (keyboard and A2 == '1') or (A2 == 0 and not keyboard):
                Q2_0.draw()
                win.flip()
                A2_0 = Response(device = device, keyboard = keyboard, quiT = quiT,\
                                                          time_search = 9000, allowed_keys = None,\
                                                          clock_items = clock_trial, row = rowI)[0]
    
                if A2_0 not in keys_4_answ:
                    A2_0 = WrongAnswer(keyboard = keyboard, question = Q2_0, answer = A2_0,\
                                     warning = wrong_answer, win = win, device = device, quiT = quiT,\
                                     rowI = rowI, keyss = keys_4_answ)
            
            bye.draw()
            win.flip()
            time.sleep(25)




    # Save results on txt every 5 trials, in case of crash I have the data anyway
    if rowI % row_save == 0 and rowI != 0:

        if keyboard:
            sheet = np.column_stack((RTs_keyboard, trial_time, items_time, is_response_right, response_key,\
                                     df.loc[:,'valid_trial'],df.loc[:,'cue_identity_def'],df.loc[:,'cue_validity_def'],\
                                     df.loc[:,'color_target'], real_target_location))
            np.savetxt(file_name, sheet, delimiter = ',', header = headers_answer, fmt='%s')
        else:
            sheet = np.column_stack((RTs_cedrus, trial_time, items_time, is_response_right, button_pressed, response_key,\
                                     df.loc[:,'valid_trial'],df.loc[:,'cue_identity_def'],df.loc[:,'cue_validity_def'],\
                                     df.loc[:,'color_target'], real_target_location))
            np.savetxt(file_name, sheet, delimiter = ',', header = headers_answer, fmt='%s')





#    question = vis.TextStim(win, text = 'What is the predictive cue? (1 2 or 3)')
#    question.draw()
#    win.flip()
#
#
#    guessedCue = event.waitKeys(keyList = Key4cues)
#
#    guessed_cues.append(guessedCue)

if not practice:
    total_time = total_clock.getTime()
    info_file_final = open('data\\part_n_' + PN + '\\info_' + PN +'.txt', 'a')
    info_file_final.write('total_time = ' + str(round(total_time/60,1)) + ' minutes')
    info_file_final.write('\ntotal_time_without_break = ' + str(round(total_time/60,1) - (round(sum(breaks)/60,1))) + ' minutes')
    info_file_final.write('\nTrials with break = ' + str(break_row))
    info_file_final.write('\nA0 = ' + str(A0) + '\nA1 = ' + str(A1))
    if A1_0 is not None:
        info_file_final.write('\nA1_0 = ' + str(A1_0))
    info_file_final.write('\nA2 = ' + str(A2))
    if A2_0 is not None:
        info_file_final.write('\nA2_0 = ' + str(A2_0))
    info_file_final.close()
    print('\n\nResponse written in txt!')


if keyboard:
    sheet = np.column_stack((RTs_keyboard, trial_time, items_time, is_response_right, response_key,\
                             df.loc[:,'valid_trial'],df.loc[:,'cue_identity_def'],df.loc[:,'cue_validity_def'],\
                             df.loc[:,'color_target'], real_target_location))
    np.savetxt(file_name, sheet, delimiter = ',', header = headers_answer, fmt='%s')
else:
    sheet = np.column_stack((RTs_cedrus, trial_time, items_time, is_response_right, button_pressed, response_key,\
                             df.loc[:,'valid_trial'],df.loc[:,'cue_identity_def'],df.loc[:,'cue_validity_def'],\
                             df.loc[:,'color_target'], real_target_location))
    np.savetxt(file_name, sheet, delimiter = ',', header = headers_answer, fmt='%s')

if practice:
    print('Reached the end of the practice succesfully!!\n\n\
Participant number is %s'%PN)
else:
    if crash:
        print('Reached the end of experiment with a crash..')
    else:
        print('Reached the end of experiment succesfully!!')

win.close()
core.quit()
quit
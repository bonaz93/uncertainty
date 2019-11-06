"""
Define functions useful for the experiment script

"""

#import numpy as np
import os
from psychopy import gui, core, visual as vis, event


#######################
##     FUNCTIONS     ##
#######################

# Just the mask for participant info.


def GUI():

    wdir = os.getcwd()

    already_exists = True


    while already_exists:
        
        info = {'Participant number':'','Subject\'s name':'','Gender':['male','female'], 'Mode':['Practice','Experiment']}
    
        infoDLG = gui.DlgFromDict(info, title = 'Welcome!')

        if not infoDLG.OK:
            
            print('CANCELLED!')
            core.quit()
            
        PN = info['Participant number']
        part_name = info['Subject\'s name']
        mode = info['Mode']

        if mode == 'Practice':
            dataframe_name = wdir + '\\data\\Practice_' + PN + '.csv'
            file_name = wdir + '\\data\\Practice_response' + PN + '.csv'
        else:
            dataframe_name = wdir + '\\data\\Dataframe_' + PN + '.csv'
            file_name = wdir + '\\data\\Response_' + PN + '.csv'



        if not os.path.isdir(wdir + '\\data'):
            os.mkdir(wdir + '\\data')


        if not os.path.isfile(file_name):
            already_exists = False

        else:
            myDlg2 = gui.Dlg(title = "FileName Error")
            myDlg2.addText('File name \'%s\' already exists!!'%file_name)
            myDlg2.show()
            
            core.quit()



        if not os.path.isfile(dataframe_name):
            myDlg2 = gui.Dlg(title = "DataFrame Error")
            myDlg2.addText('Dataframe not found at %s!!'%dataframe_name)
            myDlg2.show()

            core.quit()

    return file_name,dataframe_name, PN, part_name, mode


def Response(device, time):


    if device.is_response_device():
        
        # This should poll and clear all responses from the box before the actual response is expected
#        numb = 0
        device.poll_for_response()
        while device.has_response():
            device.clear_response_queue()
            device.poll_for_response()
#            numb += 1

#            print('number %s, cleared response %s'%(numb, re))

#        print('device has no more responses')


        clock_loc = core.Clock()
        release = False
        clock_loc.reset(time)
        device.reset_rt_timer()

        while not release:

            if clock_loc.getTime() >= 0:
                PressResponse_loc = None
                ReleaseResponse_loc = None
                break

            device.poll_for_response()

            if device.has_response():
                resp = device.get_next_response()

                if resp['pressed']:  #Is there the problem of pressing two buttons at the same time? Should not be tough..
                    PressResponse_loc = resp

                elif not resp['pressed']:
                    ReleaseResponse_loc = resp
                    release = True

                else:
                    print('Something is wrong with this response %s'%resp)


    else:
        print('device %s is not a response device!'%device)
        


    return PressResponse_loc, ReleaseResponse_loc

#The response is a python dict with the following keys:
#    pressed: True if the key was pressed, False if it was released
#    key: Response pad key pressed by the subject
#    port: Device port the response was from (typically 0)
#    time: value of the Response Time timer when the key was hit/released


#        if response.get("pressed") == True and response.get("key") == 6:
#            win.close()
#            
#        if response.get("pressed") == True:
#        cycles += 1

#C = vis.ShapeStim(win, vertices = CVert, fillColor = [0,0,0], lineWidth = 0, size = sizeItem, pos = (0,0), ori = 25, fillColorSpace = color_space)
#
#C0 = vis.Circle(win, size = size_c, radius = r, lineWidth = 0,fillColor = [0,0,0], fillColorSpace = color_space, pos = pos0)

def Instructions(part_number, part_name, win, item, cue, mode):
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
    
    message_final = 'Press a button whenever you are ready to start the real experiment, {}!'.format(part_name)

    
    
    
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
    
    textbox_final = vis.TextStim(win, text = message_final,\
                            color='black', bold = False,\
                            wrapWidth = 30.5,\
                            height = 1.2,\
                            pos=(0,0),\
                            alignVert = 'center')

    final_text = vis.TextStim(win, wrapWidth = 32, text = message_final, bold = False,pos = (0,0), height = 1.5, color = 'black')

    all_keys = ['esc','left','q','space']



    x = -5
    y = -7
    lab = ['left','right']


    counterbalance = True if part_number % 2 == 0 else False  #True when participant number is even

    if mode == 'Practice':
        if counterbalance:
            instruction1 = vis.TextStim(win, wrapWidth = 32, text = message_neutral.format(part_name, 'left', 'right'),pos = (0,0), height = .8, color = 'black') #for even participant, gap in the top = press botton 1
        else:
            instruction1 = vis.TextStim(win, wrapWidth = 32, text = message_neutral.format(part_name, 'right', 'left'),pos = (0,0), height = .8, color = 'black') #for uneven participant, gap in the top = press botton 5
            lab.reverse()
        instruction2 = vis.TextStim(win, wrapWidth = 32, text = message_explicit,pos = (0,0), height = .9, color = 'black')

        targ_message = vis.TextStim(win, text = 'DEFAULT', pos = (x-1,y-1), height = .6, color = 'black')

        instruction1.draw()
        item.pos = (x-1,y+.7)
        item.ori = 270
        item.fillColor = 'black'
        for x in range(2):
            targ_message.text = 'Target: response button on your ' + lab[x]
            item.draw()
            targ_message.draw()
            item.pos = (x+6,y+.7)
            item.ori -= 180
            targ_message.pos = (x+6,y-1)
        win.flip()
        a = event.waitKeys(keyList = all_keys)
        if quiT and ('esc' in a or 'q' in a):
            win.close()
            core.quit()
        instruction2.draw()
    #    positions = [(x,y), (x-3,y), (x-7,y)]
    #    colors = ['red','green','blue']
    #    for x in range(3):
    #        cue.fillColor = colors[x]
    #        cue.pos = positions[x]
    #        cue.draw()
        win.flip()
        a = event.waitKeys(keyList = all_keys)
        if quiT and ('esc' in a or 'q' in a):
            win.close()
            core.quit()

    else: # No more practice!
        instruction_final = vis.TextStim(win, wrapWidth = 32, text = message_final, bold = False,pos = (0,0), height = 1.5, color = 'black') #for even participant, gap in the top = press botton 1
        instruction_final.draw()
        win.flip()
        event.waitKeys()



def breaK(win):
    
    string = 'Let\'s have a break!\nPress any key to continue..'
    string2 = 'Are you ready? Press the spacebar to resume the experiment!'
    message = vis.TextStim(win, wrapWidth = 25, text = string, bold = True,pos = (0,0), height = 2, color = 'black')
    message.draw()
    win.flip()
    event.waitKeys()
    message1 = vis.TextStim(win, wrapWidth = 25, text = string2, bold = True,pos = (0,0), height = 2, color = 'black')
    message1.draw()
    win.flip()
    event.waitKeys(keyList = ['space'])


#This is a not optimal way to set the temporary cue identity and cue validity from series to series, but it works
#def SetCueIdentityValidity(i):
#
#    """ Determines the temporary cue validity and cue identity for each trial, based on cue validity values, cue identity and number of trial """
#
#    part = sum(i > cue_switches)
#    cue_validity_temp = cue_validity_all[part]
#    cue_identity_temp = cue_identity[part]
#
#    return cue_validity_temp, cue_identity_temp
#
#
#
#def OriTarget_OriVector():
#
#    """ Randomize orientation of search items and gives position of the target: choose randomly target orientation, create 12 randomly oriented distractors, insert targer orientation in a random position among distractors."""
#
#    positionTarget = np.random.choice(number_positions) #We want to save the position of the target to link the color of the target with the one of the cue.
#
#    ori_vector = np.random.choice(orientation_distractor, size = number_positions, replace = True)
#
#    ori_target = np.random.choice(orientation_target)
#
#    ori_vector[positionTarget] = ori_target
#
#
#
#    return positionTarget, ori_vector, ori_target
#
#
#
#def Pos_func():
#
#    """Gives the list of randomized positions for the search items"""
#
#    """Define position1 and position2: they are the consecutive positions "around the clock" which are colored in blue or red.
#    
#    The following is a complicated way to find the list of the positions after being randomized. This will serve the for cycle to draw all the shapes, one per each position
#    
#    E.G: in PositionReal[i] draw the first Cshape. PositionReal[0] is the position in which the drawing will start."""
#
#
#    positionFirst = np.random.choice(number_positions) #start position
#    
#    shifted_range = number_positions + positionFirst
#    positionIndex = [(x-12) if x >= 12 else x for x in shifted_range]
#
#
#
#
#
#    return positionIndex, positionFirst
#
#
#
#def CueColor(positionTarget, cue_validity_temp, cue_identity_temp, C1, C2, C3, colors = ['black','black']):
#
#    """Defines the color of each cue, basically setting randomly the two unpredictive cues and weighting the probabilities of the predictive cue of having the same color of the target"""
#
#    weights_predCue = [cue_validity_temp,1-cue_validity_temp]# Set the weights for the color of the predictive cue: the weights work as they are with the blue,
##                                                              and should be reversed with the red [because colors = ['blue','red']]
#
#    #This if_else defines the color of the target. Since the drawing starts from the index 0 of the positionReal vector, and since the drawing starts with blue
##    the first 6 positions will be blue, the next red.
#    
#    if positionTarget < 6:
#        color_target = colors[0]
#    else:
#        color_target = colors[1]
#        weights_predCue.reverse() #weights reversed because they are already ok for [color_target;color_distractors]
#
#
#    # Now the color of the cue can be chosen:
#
#    if cue_identity_temp == 1:
#        C1.fillColor = np.random.choice(colors, p = weights_predCue)
#        C2.fillColor = np.random.choice(colors)
#        C3.fillColor = np.random.choice(colors)
#
#    if cue_identity_temp == 2:
#        C1.fillColor = np.random.choice(colors)
#        C2.fillColor = np.random.choice(colors, p = weights_predCue)
#        C3.fillColor = np.random.choice(colors)
#
#    if cue_identity_temp == 3:
#        C1.fillColor = np.random.choice(colors)
#        C2.fillColor = np.random.choice(colors)
#        C3.fillColor = np.random.choice(colors, p = weights_predCue)
#
#    cue_colors = [C1.fillColor, C2.fillColor, C3.fillColor]
#    cue_colors = [0 if x == 'blue' else 1 for x in cue_colors]
#
#    while sum(cue_colors) == 3 or sum(cue_colors) == 0:
#
#        if cue_identity_temp == 1:
#            C1.fillColor = np.random.choice(colors, p = weights_predCue)
#            C2.fillColor = np.random.choice(colors)
#            C3.fillColor = np.random.choice(colors)
#
#        if cue_identity_temp == 2:
#            C1.fillColor = np.random.choice(colors)
#            C2.fillColor = np.random.choice(colors, p = weights_predCue)
#            C3.fillColor = np.random.choice(colors)
#
#        if cue_identity_temp == 3:
#            C1.fillColor = np.random.choice(colors)
#            C2.fillColor = np.random.choice(colors)
#            C3.fillColor = np.random.choice(colors, p = weights_predCue)
#
#        cue_colors = [C1.fillColor, C2.fillColor, C3.fillColor]
#        cue_colors = [0 if x == 'blue' else 1 for x in cue_colors]
#
#
#
#    return C1.fillColor, C2.fillColor, C3.fillColor, color_target


#def Response(KeyResp):   MAYBE IN THE FUTURE
#
#    """ Register participant response and RT, add the data in the respective arrays. """
#
#
#    response = event.waitKeys(keyList = KeyResp, maxWait = 5)
#
#    if response is not None:
#
#        if 'q' in response or 'escape' in response:
#            win.close()
#            core.quit()
#
#        else:
#            key_resp_def.append(response[0])
#
#        if response[0] == correct_response_temp:
#            correct_response[i] = 1
#
#        else:
#            correct_response[i] = 0
#
#    else:
#        #Should warn participant to answer more quickly
#        key_resp_def.append(-1)
#
#
#
#    response_time = my_clock.getTime()
#
#    RTs[i] = response_time
#
#    question = vis.TextStim(win, text = 'What is the predictive cue? (1 2 or 3)')
#    question.draw()
#    win.flip()
#
#
#    guessedCue = event.waitKeys(keyList = Key4cues)
#
#    guessed_cues.append(guessedCue)

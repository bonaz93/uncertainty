"""
Define functions useful for the experiment script

"""

#import numpy as np
import os, numpy as np, time
from psychopy import gui, core, visual as vis, event

print('Cshape functions imported..\n\n')
time.sleep(2)
#######################
##     FUNCTIONS     ##
#######################

# Just the mask for participant info.


def GUI():

    wdir = os.getcwd()

    already_exists = True


    while already_exists:
        
        info = {'Subject\'s name':'', 'Age':'','Gender':['Male','Female','Other'],'Participant number':'',\
                'Mode':['Practice','Experiment',],'Generate':[True,False], 'Handedness':['Right','Left']}

        infoDLG = gui.DlgFromDict(info, title = 'Welcome!')

        if not infoDLG.OK:

            print('CANCELLED!')
            core.quit()

        PN = info['Participant number']
        part_name = info['Subject\'s name']
        if len(part_name) > 0:
            if True in [a.isspace() for a in part_name]:
                part_name = part_name[:part_name.index(' ')]
            if part_name[0].islower():
                part_name = part_name.capitalize()
        mode = info['Mode']
        hand = info['Handedness']
        age = info['Age']
        gender = info['Gender']

        if mode == 'Practice':
            dataframe_name = wdir + '\\data\\part_n_' + PN + '\\Practice_' + PN + '.csv'
            file_name = wdir + '\\data\\part_n_' + PN + '\\Practice_response' + PN + '.csv'
        else:
            dataframe_name = wdir + '\\data\\part_n_' + PN + '\\Dataframe_' + PN + '.csv'
            file_name = wdir + '\\data\\part_n_' + PN + '\\Response_' + PN + '.csv'



        if not os.path.isfile(file_name):
            already_exists = False

        else:
            myDlg2 = gui.Dlg(title = "FileName Error")
            myDlg2.addText('File name \'%s\' already exists!! Change participant number or delete the file!'%file_name)
            myDlg2.show()



        if not info['Generate'] and not os.path.isfile(dataframe_name):
            myDlg2 = gui.Dlg(title = "DataFrame Error")
            myDlg2.addText('Dataframe not found at %s!!'%dataframe_name)
            myDlg2.show()

            core.quit()

    return file_name,dataframe_name, PN, part_name, mode, hand, age, gender


def Response(device, keyboard, quiT, time_search, allowed_keys, clock_items, row = -1):

    if not keyboard: #cedrus
        if device.is_response_device():
            
            # This should poll and clear all responses from the box before the actual response is expected
            device.poll_for_response()
            while device.has_response():
                device.clear_response_queue()
                device.poll_for_response()

            # Set everything to None in case I have a weird answer
            Press_key = None
            ReleaseResponse_loc = None
            Time_key = None

    
            clock_loc = core.Clock()
            release = False
            clock_loc.reset(time_search)
            device.reset_rt_timer()
    
            while not release:
    
                if clock_loc.getTime() >= 0:
                    Press_key = None
                    ReleaseResponse_loc = None
                    Time_key = None
                    break

                device.poll_for_response()
    
                if device.has_response():
                    resp = device.get_next_response()

                    if resp['pressed']:  #Is there the problem of pressing two buttons at the same time? Should not be tough..
                        Press_key = resp['key']
                        Time_key = resp['time']
                        ReleaseResponse_loc = None
#                        print('For cedrus: ',type(Press_key),type(Time_key), sep='    ')

                    elif not resp['pressed'] and Press_key is not None:
                        ReleaseResponse_loc = resp
                        release = True


                    else:
                        print('Something is wrong with this response %s at trial %s'%(resp,row))


        else:
            print('device %s is not a response device!'%device)
    else: #Keyboard
        ReleaseResponse_loc = None
        resp = event.waitKeys(maxWait = time_search, keyList = allowed_keys, timeStamped = clock_items)
        if resp is None:
            Press_key = None
            Time_key = None
        else:
            Press_key = resp[0][0]
            Time_key = resp[0][1]
#            print('For keyboard: ',type(Press_key),type(Time_key), sep='    ')


    return Press_key, Time_key, ReleaseResponse_loc

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

def Instructions(part_number, part_name, win, item, cue, mode, device, KeyResp, ori_targ, keyboard, quiT, allowed_keys,\
                 clock_items, esc_keys, cue_prot0, cue_prot1, cue_prot2, dutch):
 
    if not dutch:
        buttoN = 'the spacebar' if keyboard else 'a button'
    else:
        buttoN = 'de spatiebalk' if keyboard else 'de responsknop'

#    \n- Focus in het begin van elke trial op het centrale fixatiekruis en begin dan te zoeken van daaruit.'


    #useless clock
    clockUseless = core.Clock()
    space = 'Press {} to continue...' if not dutch else\
    'druk op {} om verder te gaan...'

    test1 = 'Press {} and respond correctly to these targets to continue!' if not dutch else\
    'Druk op {} en reageer correct op deze target stimuli om door te gaan!'

    message_1_welcome = 'Welcome to the experiment, {0}! In this visual search task, you are asked to detect as quickly\
 and accurately as possible one target among distractors.\n\nAll the items are shapes of 3 different random colors (red, blue or green - changing randomly),\
 with a gap on one side:\
    \n\n- Target items have a gap on either the upper or the lower part.\
    \n- Distractors have a gap on the left or on the right.' if not dutch else\
    'Welkom in dit experiment! In deze visuele zoektaak zal je zo snel\
 en accuraat mogelijk een target moeten detecteren tussen distractoren (afleiders). Deze stimuli zijn vormen in 3 verschillende kleuren (rood, blauw of groen) met een opening aan één kant:\
    \n\n- Target stimuli hebben ofwel aan de bovenkant ofwel aan onderkant een opening\
    \n- Distractoren hebben ofwel aan de linkerkant ofwel aan de rechterkant een opening.'

    message_2_target = 'Please look at the fixation point in the center of the screen and start your search from there!\nThe target will be always present and you have to respond to its orientation in this way:\
    \n\n- Press the button on the top with your {} index finger if the gap is on the top of the shape.\
    \n- Press the button on the bottom with your {} index finger if the gap is on the bottom of the shape.' if not dutch else\
    'Kijk naar het fixatiekruis in het midden van het scherm tot de stimuli op het scherm verschijnen, begin dan onmiddelijk met zoeken!\
 Er zal altijd een target aanwezig zijn en je moet reageren op de oriëntatie van deze target:\
    \n\n- Duw met je wijsvinger op de bovenste toets als de opening aan de bovenkant is.\
    \n- Duw met je wijsvinger op de onderste toets als de opening aan de onderkant is.'


    message_3_cues = 'Before the search, a set of 3 colored cues will appear (colors will change every trial). Please note that:\
    \n\n- Only ONE of the 3 cues will often have the same color of the target, helping you in the visual search!\
    \n\n- The other 2 cues will be colored randomly.' if not dutch else\
    'Voor de zoektaak begint zal een set van 3 gekleurde cues verschijnen (kleuren veranderen van trial tot trial). Let op dat:\
    \n\n- Enkel ÉÉN van de 3 cues een correct voorspellende cue is, en enkel deze cue heeft hetzelfde kleur als de target. Dit kan je helpen in de visuele zoektaak.\
    \n- De andere 2 cues zullen een willekeurig kleur hebben.'


    message_objective = '**You have to guess which of the three cues is the one that is OFTEN colored as the target in order to make a quick detection!**'if not dutch else\
    '**Je zal moeten raden welk van de 3 cues de correct voorspellende cue is. Dus, welke cue VAAK hetzelfde kleur heeft als de target om zo de target snel te kunnen detecteren.**'

    message_4_switch = 'The cue often colored as the target will not remain the same for the whole experiment (for example, it can switch \
from the right position to the top one after some trials). Generally, this cue change will happen a few times within the experiment (but note that it won\'t change too often - NOT every few trials...' if not dutch else\
'Welke cue vaak dezelfde kleur heeft als de target, zal niet gedurende het hele experiment hetzelfde blijven (het kan bijvoorbeeld na \
enkele trials veranderen van de rechter positie naar de bovenste positie). Over het algemeen zal deze cue verandering een paar\
 keer binnen elk blok gebeuren (maar let op: het zal niet te vaak veranderen).'

    message_5_questions = 'Please ask any question now if something is not clear!' if not dutch else\
    'Is alles duidelijk? Zo niet, stel alsjeblieft vragen aan de proefleider!'

    message_6 = 'You will start with some practice trials as soon as you press a button..' if not dutch else\
    'Druk op een knop om te beginnen met enkele oefentrials.'
 
    recap_message = 'Just a few things before we get started:\n\n\n\
    - Remember to use the reliable cue to speed up the visual search (respond as fast and as accurately as possible)\n\n\
    - Try to notice if the cue you are using is reliable or not\n\n\
    - Always look at the fixation cross in the center before the search!' if not dutch else\
    'Een paar dingen voordat we beginnen:\n\n\n\
    - Vergeet niet de betrouwbare cue te gebruiken om het visueel zoeken te versnellen (reageer zo snel en zo accuraat mogelijk).\n\n\
    - Probeer op te merken of de cue die je gebruikt betrouwbaar is of niet.\n\n\
    - Kijk altijd naar het fixatiekreus in het midden voor het zoeken!'


    message_final = 'Press a button whenever you are ready to start the real experiment, {}!'.format(part_name) if not dutch else\
    'Druk op een knop wanneer je klaar bent om het echte experiment te starten, {}!'.format(part_name)

    wrap = 32.5
    triangle_side = 4
    yT = ((triangle_side**2-(triangle_side/2)**2)**(1/2))/2

    move_right = 4
    move_down = 3 

    pos1 = (0,yT)

    def Wait_and_respond(message, device,keyboard,quiT, allowed_keys,message2 = None, wait = 8,\
                         time_search = 90, clock_items = clockUseless):
        time.sleep(wait)
        if message is not None:
            message.draw()
            if message2 is not None:
                message2.draw()
            win.flip()
        Press_key, Time_key, ReleaseResponse_loc = Response(device = device, keyboard = keyboard, quiT = quiT,\
                                                                time_search = 90, allowed_keys = allowed_keys,\
                                                                clock_items = clockUseless)
        if quiT and Press_key in esc_keys:
            print('QUIT! Key %s'%Press_key)
            win.close()
            core.quit()
        return Press_key



#    practicemessage = vis.TextStim(win, text = practice_message.format(buttoN),\
#                            color='white',\
#                            wrapWidth = wrap,\
#                            height = .8,\
#                            pos=(0,-8.5),\
#                            alignVert = 'bottom')


    objmessage = vis.TextStim(win, text = message_objective,\
                            color='black',\
                            wrapWidth = wrap,\
                            height = 1,\
                            pos=(0,0),\
                            alignVert = 'bottom', bold = True)

    cuelabel = vis.TextStim(win, text = 'The cues',\
                            color='black',\
                            wrapWidth = wrap,\
                            height = .7,\
                            pos=((pos1[0] - move_right,- pos1[1] - move_down - 2)),\
                            alignVert = 'bottom', bold = False)

    spacetext = vis.TextStim(win, text = space.format(buttoN),\
                            color='white',\
                            wrapWidth = wrap,\
                            height = .5,\
                            pos=(0,-8.5),\
                            alignVert = 'bottom')

    testtext = vis.TextStim(win, text = test1.format(buttoN),\
                            color='white',\
                            wrapWidth = wrap,\
                            height = .8,\
                            pos=(0,-7.5),\
                            alignVert = 'bottom')

    textbox_1 = vis.TextStim(win, text = message_1_welcome.format(part_name),\
                            color='black',\
                            wrapWidth = wrap,\
                            height = .9,\
                            pos=(0,0),\
                            alignVert = 'center')

    textbox_2 = vis.TextStim(win, text = 'def',\
                            color='black',\
                            wrapWidth = wrap,\
                            height = .9,\
                            pos=(0,4),\
                            alignVert = 'center')

    textbox_3 = vis.TextStim(win, text = message_3_cues,\
                            color='black',\
                            wrapWidth = wrap,\
                            height = .9,\
                            pos=(0,5),\
                            alignVert = 'center')

    textbox_4 = vis.TextStim(win, text = message_4_switch,\
                            color='black',\
                            wrapWidth = wrap,\
                            height = .9,\
                            pos=(0,0),\
                            alignVert = 'center')

    textbox_5 = vis.TextStim(win, text = message_5_questions,\
                            color='black', bold = True,\
                            wrapWidth = wrap,\
                            height = 1.2,\
                            pos=(0,0),\
                            alignVert = 'center')
                            
    textbox_6 = vis.TextStim(win, text = message_6,\
                            color='black', bold = False,\
                            wrapWidth = wrap,\
                            height = .8,\
                            pos=(0,-4),\
                            alignVert = 'center')

    
    recap = vis.TextStim(win, text = recap_message,\
                        color='black', bold = False,\
                        wrapWidth = wrap,\
                        height = 1,\
                        pos=(0,0),\
                        alignVert = 'center')


    textbox_final = vis.TextStim(win, text = message_final,\
                            color='black', bold = False,\
                            wrapWidth = wrap,\
                            height = 1.2,\
                            pos=(0,0),\
                            alignVert = 'center')
    
    



    lab = ['left','right']


    counterbalance = True if part_number % 2 == 0 else False  #True when participant number is even

    if mode == 'Practice':
        if counterbalance:
            textbox_2.text = message_2_target.format(lab[0], lab[1]) #for even participant, switch hands (left index on the top)
        else:
            textbox_2.text = message_2_target.format(lab[1], lab[0]) # for uneven participant, switch hands (right index on the top)
        textbox_1.draw()
        win.flip()
        Wait_and_respond(message = spacetext, device = device, keyboard = keyboard, quiT = quiT,\
                         allowed_keys = allowed_keys, message2 = textbox_1)
        textbox_2.draw()
        win.flip()
        Wait_and_respond(message = testtext, device = device, keyboard = keyboard, quiT = quiT,\
                         allowed_keys = allowed_keys,message2 = textbox_2)

        item.pos = (0,-5)
        ori = ori_targ*2
        np.random.shuffle(ori)
        right_resp = [KeyResp[0] if r == 90 else KeyResp[1] for r in ori]
        item.fillColor = 'black'
        count = 0
        while count < 4:
            for x in range(4):
                time.sleep(.7)
                item.ori = ori[x]
                item.draw()
                textbox_2.draw()
                testtext.text = 'Respond correctly to these targets to continue!' if not dutch else\
                'Reageer correct op deze target stimuli om door te gaan!'
                testtext.draw()
                win.flip()
                Press_key = Wait_and_respond(message = None, device = device, keyboard = keyboard, quiT = quiT, allowed_keys = allowed_keys, wait = 0)

                if Press_key == right_resp[x]:
                    item.fillColor = 'lime'
                    testtext.draw()
                    textbox_2.draw()
                    item.draw()
                    win.flip()
                    time.sleep(.3)
                    count +=1
                else:
                    item.fillColor = 'crimson'
                    testtext.draw()
                    textbox_2.draw()
                    item.draw()
                    win.flip()
                    time.sleep(.3)
                    count =- 2
                item.fillColor = 'black'

        textbox_3.draw()
        cue_prot0.draw()
        cue_prot1.draw()
        cue_prot2.draw()
        cuelabel.draw()
        win.flip()
        textbox_3.draw()
        cue_prot0.draw()
        cue_prot1.draw()
        cue_prot2.draw()
        cuelabel.draw()
        Wait_and_respond(message = spacetext, device = device, keyboard = keyboard, quiT = quiT,\
                         allowed_keys = allowed_keys, wait = 10)
        objmessage.draw()
        win.flip()
        Wait_and_respond(message = objmessage, device = device, keyboard = keyboard, quiT = quiT,\
                        allowed_keys = allowed_keys, message2 = spacetext ,wait = 4)

        textbox_4.draw()
        win.flip()
        Wait_and_respond(message = textbox_4, device = device, keyboard = keyboard, quiT = quiT,\
                         allowed_keys = allowed_keys, message2 = spacetext, wait = 10)
        textbox_5.draw()
        win.flip()
        Wait_and_respond(message = textbox_5, device = device, keyboard = keyboard, quiT = quiT,\
                         allowed_keys = allowed_keys, message2 = textbox_6, wait = 10)

    else: #real experiment starting
        recap.draw()
        win.flip()
        Wait_and_respond(message = recap, device = device, keyboard = keyboard, quiT = quiT,\
                         allowed_keys = allowed_keys, message2 = spacetext, wait = 10)
        textbox_final.draw()
        win.flip()
        Wait_and_respond(message = textbox_final, device = device, keyboard = keyboard, quiT = quiT,\
                         allowed_keys = allowed_keys, message2 = None, wait = .1)





def breaK(win,device, keyboard, quiT, allowed_keys, clock_items,row, response, rt,dutch, time_search = 500000, string1 = 'default',\
          crash = False, row_start = 0):

    if crash:
        acc = len(response[response == 1])/(row-row_start)*100
        rts = np.mean(rt[row_start:row])

    else:
        acc = len(response[response == 1])/(row)*100
        rts = np.mean(rt[:row])

#    err = len(response[response == 0])/(row)*100
#    miss = len(response[response == -1])/(row)*100

    string = 'Let\'s have a break!\n\nYour mean reaction time is {}ms!\n\n\
You accuracy is {}%!' if not dutch else \
    'Laten we een pauze nemen! Je gemiddelde reactietijd is {}ms!\n\nJe nauwkeurigheid is {}%!'
    string2 = 'Are you ready? Press a button to resume the experiment!' if not dutch else\
    'Ben je er klaar voor? Druk op een knop om het experiment te hervatten!'

    message = vis.TextStim(win, wrapWidth = 30, text = 'DEF', bold = False,pos = (0,0), height = 2, color = 'black')
    if keyboard:
        message.text = string.format(int(round(rts*1000)),round(acc))
    else:
        message.text = string.format(int(round(rts)),round(acc))
    message.draw()
    win.flip()
    Response(device, keyboard, quiT, time_search, allowed_keys, clock_items)
    message.text = string1
    message.wrapWidth = 32
    message.height = 1
    message.draw()
    win.flip()
    time.sleep(8)
    Response(device, keyboard, quiT, time_search, allowed_keys, clock_items)
    message1 = vis.TextStim(win, wrapWidth = 25, text = string2, bold = True,pos = (0,0), height = 2, color = 'black')
    message1.draw()
    win.flip()
    Response(device, keyboard, quiT, time_search, allowed_keys, clock_items)

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

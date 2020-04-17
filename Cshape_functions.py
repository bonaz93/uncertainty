"""
Define functions useful for the experiment script

"""

import os
import time
import numpy as np

from psychopy import visual as vis
from psychopy import gui, core, event

if __name__ != '__main__':
    print('Cshape_functions imported..\n\n')
    time.sleep(.5)

#######################
##     FUNCTIONS     ##
#######################

# Just the mask for participant info.


def GUI(implicit, practice, wdir):

    already_exists = True

    while already_exists:
        if not practice:
            info = {
                'Participant\'s name': '',
                'Age': '',
                'Gender': ['Male', 'Female', 'Other'],
                'Participant number': '',
                'Handedness': ['Right', 'Left']
            }
        else:
            info = {'Participant\'s name': '', 'Participant number': ''}

        infoDLG = gui.DlgFromDict(info, title='Welcome!')

        if not infoDLG.OK:
            print('CANCELLED!')
            core.quit()

        PN = info['Participant number']
        part_name = info['Participant\'s name']
        if len(part_name) > 0:
            if True in [a.isspace() for a in part_name]:
                part_name = part_name[:part_name.index(' ')]
            if part_name[0].islower():
                part_name = part_name.capitalize()

        if not practice:
            hand = info['Handedness']
            age = info['Age']
            gender = info['Gender']

        if practice:
            dataframe_name = wdir + '\\data\\part_n_' + PN + '\\Practice' +\
            ('_implicit_' if implicit else '_') + PN + '.csv'
            file_name = wdir + '\\data\\part_n_' + PN + '\\Practice_response' +\
            ('_implicit_' if implicit else '_') + PN + '.csv'
        else:
            dataframe_name = wdir + '\\data\\part_n_' + PN + '\\Dataframe' +\
            ('_implicit_' if implicit else '_') + PN + '.csv'
            file_name = wdir + '\\data\\part_n_' + PN + '\\Response' +\
            ('_implicit_' if implicit else '_') + PN + '.csv'

        if not os.path.isfile(file_name):
            already_exists = False

        else:
            myDlg2 = gui.Dlg(title="FileName Error")
            myDlg2.addText(
                'File name \'%s\' already exists!! Change participant number or delete the file!'
                % file_name)
            myDlg2.show()

        if not os.path.isfile(dataframe_name):
            myDlg2 = gui.Dlg(title="DataFrame Error")
            myDlg2.addText('Dataframe not found at %s!!' % dataframe_name)
            myDlg2.show()

            core.quit()

    if not practice:
        return file_name, dataframe_name, PN, part_name, hand, age, gender

    return file_name, dataframe_name, PN, part_name


def Response(device, keyboard, time_search, allowed_keys, clock_items, row=-1):

    if not keyboard:  #cedrus
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

            timer = core.Clock()
            release = False

            timer.reset(time_search)
            device.reset_rt_timer()

            while not release:

                if timer.getTime() >= 0:
                    Press_key = None
                    ReleaseResponse_loc = None
                    Time_key = None
                    break

                device.poll_for_response()

                if device.has_response():
                    resp = device.get_next_response()

                    if resp['pressed']:
                        Press_key = resp['key']
                        Time_key = resp['time']
                        ReleaseResponse_loc = None

                    elif not resp['pressed'] and Press_key is not None:
                        ReleaseResponse_loc = resp
                        release = True

                    else:
                        print('Something is wrong with this response %s at trial %s'\
                              %(resp,row))

        else:
            print('device %s is not a response device!' % device)
    else:  #keyboard
        ReleaseResponse_loc = None
        resp = event.waitKeys(maxWait=time_search,
                              keyList=allowed_keys,
                              timeStamped=clock_items)
        if resp is None:
            Press_key = None
            Time_key = None
        else:
            Press_key = resp[0][0]
            Time_key = resp[0][1]

    return Press_key, Time_key, ReleaseResponse_loc


#The cedrus response is a python dict with the following keys:
#    pressed: True if the key was pressed, False if it was released
#    key: Response pad key pressed by the subject
#    port: Device port the response was from (typically 0)
#    time: value of the Response Time timer when the key was hit/released


def Instructions(part_number, part_name, win, item, device, KeyResp, ori_targ,
                 keyboard, quiT, allowed_keys, esc_keys, cue_prot0, cue_prot1,
                 cue_prot2, dutch, message_dict, practice, implicit):

    clockUseless = core.Clock()

    def Wait_and_respond(message,
                         device,
                         keyboard,
                         allowed_keys,
                         message2=None,
                         wait=8):
        time.sleep(wait)
        if message is not None:
            message.draw()
            if message2 is not None:
                message2.draw()
            win.flip()
        Press_key, Time_key, ReleaseResponse_loc = Response(
            device=device,
            keyboard=keyboard,
            time_search=900,
            allowed_keys=allowed_keys,
            clock_items=clockUseless)
        if quiT and Press_key in esc_keys:
            print('QUIT! Key %s' % Press_key)
            win.close()
            core.quit()
        return Press_key

    wrap = 32.5

    #True when participant number is even, to switch index fingers on buttons
    counterbalance = True if part_number % 2 == 0 else False
    lab = ['left', 'right'] if not dutch else ['linker', 'rechter']

    if not implicit:
        recap_text = message_dict['recap_message']
    elif counterbalance:
        recap_text = message_dict['recap_message'].format(lab[0], lab[1])
    else:
        recap_text = message_dict['recap_message'].format(lab[1], lab[0])

    #Parameters for cue positions in instructions
    if not implicit:
        triangle_side = 4
        move_right = 4
        move_down = 3
        yT = ((triangle_side**2 - (triangle_side / 2)**2)**(1 / 2)) / 2
        pos1 = (0, yT)

        cuelabel = vis.TextStim(win,
                                text='The cues' if not dutch else 'De cues',
                                color='black',
                                wrapWidth=wrap,
                                height=.7,
                                pos=((pos1[0] - move_right,
                                      -pos1[1] - move_down - 2)),
                                anchorVert='bottom',
                                bold=False)
        objmessage = vis.TextStim(win,
                                  text=message_dict['message_objective'],
                                  color='black',
                                  wrapWidth=wrap,
                                  height=1,
                                  pos=(0, 0),
                                  anchorVert='bottom',
                                  bold=True)
        textbox_3 = vis.TextStim(win,
                                 text=message_dict['message_3_cues'],
                                 color='black',
                                 wrapWidth=wrap,
                                 height=.9,
                                 pos=(0, 5),
                                 anchorVert='center')
        textbox_4 = vis.TextStim(win,
                                 text=message_dict['message_4_switch'],
                                 color='black',
                                 wrapWidth=wrap,
                                 height=.9,
                                 pos=(0, 0),
                                 anchorVert='center')

    recap = vis.TextStim(win,
                         text=recap_text,
                         color='black',
                         bold=False,
                         wrapWidth=wrap,
                         height=1,
                         pos=(0, 0),
                         anchorVert='center')
    spacetext = vis.TextStim(win,
                             text=message_dict['space'].format(
                                 message_dict['buttoN']),
                             color='white',
                             wrapWidth=wrap,
                             height=.5,
                             pos=(0, -8.5),
                             anchorVert='bottom')
    testtext = vis.TextStim(win,
                            text=message_dict['test1'].format(
                                message_dict['buttoN']),
                            color='white',
                            wrapWidth=wrap,
                            height=.8,
                            pos=(0, -7.5),
                            anchorVert='bottom')
    textbox_1 = vis.TextStim(
        win,
        text=message_dict['message_1_welcome'].format(part_name),
        color='black',
        wrapWidth=wrap,
        height=.9,
        pos=(0, 0),
        anchorVert='center')
    textbox_2 = vis.TextStim(win,
                             text='def',
                             color='black',
                             wrapWidth=wrap,
                             height=.9,
                             pos=(0, 4),
                             anchorVert='center')
    textbox_5 = vis.TextStim(win,
                             text=message_dict['message_5_questions'],
                             color='black',
                             bold=True,
                             wrapWidth=wrap,
                             height=1.2,
                             pos=(0, 0),
                             anchorVert='center')
    textbox_6 = vis.TextStim(win,
                             text=message_dict['message_6'],
                             color='black',
                             bold=False,
                             wrapWidth=wrap,
                             height=.8,
                             pos=(0, -4),
                             anchorVert='center')
    textbox_final = vis.TextStim(
        win,
        text=message_dict['message_final'].format(part_name),
        color='black',
        bold=False,
        wrapWidth=wrap,
        height=1.2,
        pos=(0, 0),
        anchorVert='center')

    if practice:
        if counterbalance:
            textbox_2.text = message_dict['message_2_target'].format(
                lab[0], lab[1]
            )  #for even participant, switch hands (left index on the top)
        else:
            textbox_2.text = message_dict['message_2_target'].format(
                lab[1], lab[0]
            )  # for uneven participant, switch hands (right index on the top)
        textbox_1.draw()
        win.flip()
        Wait_and_respond(message=spacetext,
                         device=device,
                         keyboard=keyboard,
                         allowed_keys=allowed_keys,
                         message2=textbox_1)
        textbox_2.draw()
        win.flip()
        Wait_and_respond(message=testtext,
                         device=device,
                         keyboard=keyboard,
                         allowed_keys=allowed_keys,
                         message2=textbox_2)

        item.pos = (0, -5)
        ori = ori_targ * 2
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
                testtext.text = 'Respond correctly to these targets to continue!'\
                                if not dutch else 'Reageer correct op deze target stimuli om door te gaan!'
                testtext.draw()
                win.flip()
                Press_key = Wait_and_respond(message=None,
                                             device=device,
                                             keyboard=keyboard,
                                             allowed_keys=allowed_keys,
                                             wait=0)

                if Press_key == right_resp[x]:
                    item.fillColor = 'lime'
                    testtext.draw()
                    textbox_2.draw()
                    item.draw()
                    win.flip()
                    time.sleep(.3)
                    count += 1
                else:
                    item.fillColor = 'crimson'
                    testtext.draw()
                    textbox_2.draw()
                    item.draw()
                    win.flip()
                    time.sleep(.3)
                    count = -2
                item.fillColor = 'black'

        if not implicit:
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
            Wait_and_respond(message=spacetext,
                             device=device,
                             keyboard=keyboard,
                             allowed_keys=allowed_keys,
                             wait=10)
            objmessage.draw()
            win.flip()
            Wait_and_respond(message=objmessage,
                             device=device,
                             keyboard=keyboard,
                             allowed_keys=allowed_keys,
                             message2=spacetext,
                             wait=4)

            textbox_4.draw()
            win.flip()
            Wait_and_respond(message=textbox_4,
                             device=device,
                             keyboard=keyboard,
                             allowed_keys=allowed_keys,
                             message2=spacetext,
                             wait=10)
        textbox_5.draw()
        win.flip()
        Wait_and_respond(message=textbox_5,
                         device=device,
                         keyboard=keyboard,
                         allowed_keys=allowed_keys,
                         message2=textbox_6,
                         wait=10)

    else:  #real experiment starting
        recap.draw()
        win.flip()
        Wait_and_respond(message=recap,
                         device=device,
                         keyboard=keyboard,
                         allowed_keys=allowed_keys,
                         message2=spacetext,
                         wait=10)
        textbox_final.draw()
        win.flip()
        Wait_and_respond(message=textbox_final,
                         device=device,
                         keyboard=keyboard,
                         allowed_keys=allowed_keys,
                         message2=None,
                         wait=.1)


def breaK(implicit,
          win,
          device,
          keyboard,
          allowed_keys,
          clock_items,
          row,
          response,
          rt,
          dutch,
          crash,
          message_dict,
          time_search=500000,
          row_start=0):

    if crash:
        acc = len(response[response == 1]) / (row - row_start) * 100
        rts = np.mean(rt[rt > 0][row_start:row])

    else:
        acc = len(response[response == 1]) / (row) * 100
        rts = np.mean(rt[rt > 0][:row])

    string = 'Let\'s have a break!\n\nYour mean reaction time is {}ms!\n\n\
You accuracy is {}%!'                      if not dutch else \
    'Laten we een pauze nemen! Je gemiddelde reactietijd is {}ms!\n\nJe nauwkeurigheid is {}%!'
    string2 = 'Are you ready? Press a button to resume the experiment!' if not dutch else\
    'Ben je er klaar voor? Druk op een knop om het experiment te hervatten!'

    message = vis.TextStim(win,
                           wrapWidth=30,
                           text='DEF',
                           bold=False,
                           pos=(0, 0),
                           height=2,
                           color='black')
    if keyboard:
        message.text = string.format(int(round(rts * 1000)), round(acc))
    else:
        message.text = string.format(int(round(rts)), round(acc))
    message.draw()
    win.flip()
    Response(device, keyboard, time_search, allowed_keys, clock_items)
    if not implicit:
        message.text = message_dict['important_message_remember']
        message.wrapWidth = 32
        message.height = 1
        message.draw()
        win.flip()
        time.sleep(8)
        Response(device, keyboard, time_search, allowed_keys, clock_items)
    message1 = vis.TextStim(win,
                            wrapWidth=25,
                            text=string2,
                            bold=True,
                            pos=(0, 0),
                            height=2,
                            color='black')
    message1.draw()
    win.flip()
    Response(device, keyboard, time_search, allowed_keys, clock_items)


#define function for translating colors for draw search array
def C_color_position(positions, position_target, color_labels, color_target):

    position_arr = np.split(positions, len(color_labels))
    #Return in which chunk of positions is the target
    index_position_target = [position_target in i
                             for i in position_arr].index(True)
    index_color = color_labels.index(color_target)

    while index_position_target != index_color:
        color_labels = color_labels[1:] + color_labels[:1]
        index_color = color_labels.index(color_target)

    final_colors = []
    for pos, color in zip(position_arr, color_labels):
        for _ in pos:
            final_colors.append(color)

    return final_colors


def WrongAnswer(keyboard, question, answer, warning, win, device, rowI, keyss):
    useless_clock = core.Clock()
    if keyboard:
        while answer not in keyss:
            question.draw()
            warning.draw()
            win.flip()
            answer = Response(device = device, keyboard = keyboard,
                                  time_search = 9000, allowed_keys = None,\
                                  clock_items = useless_clock, row = rowI)[0]
    else:
        while answer not in keyss:
            question.draw()
            warning.draw()
            win.flip()
            answer = Response(device = device, keyboard = keyboard,
                                  time_search = 9000, allowed_keys = None,\
                                  clock_items = useless_clock, row = rowI)[0]
    return answer

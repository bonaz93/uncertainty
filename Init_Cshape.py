# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 12:18:29 2019

@author: Jacopo

Only set important variables once, for Randomization and experimental script. 
Also turn on/off some control on randomizations, decide which is the response device, etc.."""


import random, shutil, os, time
print('Init script is being executed!!\n')
time.sleep(2)
from psychopy import monitors
from Cshape_functions import GUI


file_name, dataframe_name, PN, part_name, mode, hand, age, gender = GUI()

##Language
dutch = True

monitor = 'jac'  #set 'exp' for experiment, 'jac' for my latitude, else 'default'

# Saving txt after how many trials?
row_save = 5

# After how many minutes should we do a break?
break_time = 7

participants = range(0,1) #list of dataframes we want to create dataframe for each participant


## Randomization controls?
row_check = 10 # What is the default chunk of lines to check?
control_target_cue_match = False
control_same_color = True #Is it possible to have three cues of the same color?

## Possible to quit experiment?
quiT = True

# Response device: keyboard or Cedrus?
keyboard = True


# Set the preferred color space, adjust the labels accordingly. To use gammacorrection and isoluminant stimuli, RGB is needed. To test on different monitors use HSV.
color_space = 'hsv'

if color_space == 'hsv':
    color_labels = [(240, 1, 1), (0, 1, 1), (90, 1, 1)]
elif color_space == 'rgb':
    color_labels = [(-1,-1,1), (-1+(255*9.6/26*(2/255)),-1,-1), (-1,-1+(255*9.6/79.9*(2/255)),-1)]
else:
    color_labels = ['blue','red', 'green']

##Practice or real dataframe?
practice = True if mode =='Practice' else False
##Hints (debug and general idea of the procedure)?
if not practice:
    hints = False
else:
    hints = True

## CRASH? Edit the line to start again in the dataframe. Rename the response dataframe and the info file.

crash = False
if crash:
    row_crash = 45
else:
    row_crash = 0


orientation_target = [0,1] #[90,270] # Only turned down/up
orientation_distractor = [0,1] #[0,180] # Only turned right/left

# Cue validity levels
cue_validity_0 = .76
cue_validity_1 = .83
cue_validity_2 = .9

trials_total = 30 if practice else 210 #Number of rows in the dataframe and of repetitions in the experimental script
series = 1 if practice else 3# Number of series in total - one serie is a set of trials in which cue_identity and cue_validity do NOT change

number_positions = 12  # Search array items
number_distractors = number_positions - 1

colors = [0,1,2]  #['blue','red', 'green']


if keyboard:
    KeyResp = ['down','up']
    esc_keys = ['q', 'escape']
    allowed_keys = KeyResp + esc_keys + ['space']
    headers_answer = 'Reaction_times_Keyboard,Total_trial_time,Items_time,Placeholder_time,Cue_time,is_response_right,response_key,valid_trial, cue_identity, cue_validity'

else:
    KeyResp = [0,6]   #buttons of the cedrus box for response
    allowed_keys = None
    esc_keys = [3]
    headers_answer = 'Reaction_times_Cedrus,Total_trial_time,Items_time,Placeholder_time,Cue_time,is_response_right,Button_pressed,response_key, valid_trial, cue_identity, cue_validity'



headers = ['position_target','color_target','color_cue0','color_cue1','color_cue2','ori_target','ori_distractor_0','ori_distractor_1','ori_distractor_2',
           'ori_distractor_3','ori_distractor_4','ori_distractor_5','ori_distractor_6','ori_distractor_7',
           'ori_distractor_8','ori_distractor_9','ori_distractor_10','ori_distractor_11','cue_identity_def','cue_validity_def','valid_trial','correct_response', 'Start_position']



###timings

refresh_rate = 60  # in Hertz

def ms_to_frames(ms, rate = refresh_rate):
    return round(ms * rate/1000)

if practice:
    time_placeholder = range(ms_to_frames(500))
    time_cues = range(ms_to_frames(5000))
    time_fixation = range(random.randrange(ms_to_frames(500),ms_to_frames(1000), ms_to_frames(100)))   # Random variable must be called everytime inside the script..?
    time_search = 8
    time_iti = range(random.randrange(ms_to_frames(500),ms_to_frames(1000), ms_to_frames(100)))   # Random variable must be called everytime inside the script..?
else:
    time_placeholder = range(ms_to_frames(500))
    time_cues = range(ms_to_frames(800))
    time_fixation = range(random.randrange(ms_to_frames(500),ms_to_frames(1000), ms_to_frames(100)))   # Random variable must be called everytime inside the script..?
    time_search = 2.5
    time_iti = range(random.randrange(ms_to_frames(500),ms_to_frames(1000), ms_to_frames(100)))   # Random variable must be called everytime inside the script..?




    ### MONITORS.. I can try to laod the json calibration here C:\Users\pp02\AppData\Roaming\psychopy3\monitors
    # Putting the gamma calibration file in the working directory should upload it to the right place in the computer.
    
gamma_path = 'C:\\Users\\pp02\\AppData\\Roaming\\psychopy3\\monitors\\'
gamma_configuration_name = 'BenQ.json'
if monitor == 'default':
    mon = monitors.Monitor('testMonitor')
elif monitor == 'exp':
    if os.path.isfile(os.path.join(os.getcwd(), 'BenQ.json')) and not os.path.isfile(os.path.normpath(os.path.join(gamma_path, gamma_configuration_name))):
        print('Gamma configuration file found! Will move it in the right place\n')
        shutil.copy(os.path.join(os.getcwd(), gamma_configuration_name), os.path.normpath(gamma_path))
    elif not os.path.isfile(os.path.join(os.getcwd(), gamma_configuration_name)):
        print('Gamma configuration file not found!\n')
    elif os.path.isfile(os.path.normpath(os.path.join(gamma_path, gamma_configuration_name))):
        print('Gamma configuration file already present!\n\n')
    time.sleep(2)
    mon = monitors.Monitor(name = 'BenQ', width = 53.1, distance = 60)
    mon.setSizePix([1920,1080])
    mon.setCurrent('2019_10_30 16:27_gamma')
elif monitor == 'jac':
    mon = monitors.Monitor('Latitude_Jacopo')
else:
    raise Exception('Monitor name not set correctly!!')




### MESSAGES and translation
    
if keyboard:
    wrong_key_text = 'Wrong button, please only respond with up or down arrow' if not dutch else\
    'Verkeerde knop, reageer alsjeblieft alleen met de bovenste of de onderste toets'
else:
    wrong_key_text = 'Wrong button, please only respond with the first and last button' if not dutch else\
    'Verkeerde knop, reageer alsjeblieft alleen met de bovenste of de onderste toets'

late_answer_text = 'Try to respond faster!' if not dutch else 'Probeer om sneller te reageren!'

switch_text = 'The position of the predictive cue is about to change!' if not dutch else 'De positie van de voorspellende cue gaat bijna veranderen!'

no_more_mess_text = 'No more hints! Can you follow the right cue?' if not dutch else'Geen hints meer! Kun je de juiste cue volgen?'

end_practice = 'Good job! As you may have noticed, very often but not always the reliable cue has the same \
color of the target!\n\nIn the real experiment you will have no hints and you will need to infer when the reliable\
 cue has changed position to make a good performance :)' if not dutch else 'Goed zo! Zoals je misschien gemerkt hebt heeft de\
 betrouwbare cue vaak, maar niet altijd, dezelfde kleur als de target! In het echte experiment heb je geen hints en moet je raden\
 wanneer de betrouwbare cue van positie is veranderd om een goede prestatie te leveren :)'
    
neg_feedback_text = 'Wrong answer! Up for gap in the top, down for gap in the bottom!' if not dutch else 'Verkeerd antwoord!\
 Gebruik de bovenste toets als de opening aan de bovenkant is, en de onderste toets als de opening aan de onderkant is.'
 
hint_text = 'The reliable cue is in the {} position' if not dutch else 'De betrouwbare cue staat in de {} positie'

bye_text = 'Thanks for participating and goodbye!' if not dutch else 'Bedankt voor uw deelname en tot ziens.'

 #TO BE TRANSLATED BETTER?
string1 = 'Always try to understand which of the three cues is the reliable one (more often colored as the target) and use it to find the target faster!\n\n\
 And remember that:\
\n\n\n - The reliable cue will not *always* be of the same color of the target, but *most of the times* it will!\
\n\n\n - The reliable cue can change position after a certain amount of trials' if not dutch else\
'Probeer te begrijpen welke van de drie signalen de betrouwbare is (vaker gekleurd als het doelwit) en gebruik het om\
 het doel sneller te vinden!\
 En onthoud dat:\
\n\n\n - De betrouwbare cue zal niet *altijd* van dezelfde kleur zijn als het doelwit, maar *meestal* wel!\
\n\n\n - De betrouwbare cue zal van positie veranderen na een variabel aantal trials.'

 #TO BE TRANSLATED BETTER?
invalid_hint = 'This trial was invalid! The reliable cue was not of the same color of the target, but this doesn\'t necessarly means\
 that it switched position!' if not dutch else\
'Deze trial was ongeldig! De betrouwbare cue was niet van dezelfde kleur als het doelwit, \
maar dit betekent niet noodzakelijkerwijs dat het van plaats veranderd is!'
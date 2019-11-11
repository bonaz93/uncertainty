# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 12:18:29 2019

@author: Jacopo

Only set important variables once, for Randomization and experimental script. 
Also turn on/off some control on randomizations, decide which is the response device, etc.."""


import random, shutil, os, time
from psychopy import monitors
from Cshape_functions import GUI

file_name, dataframe_name, PN, part_name, mode, hand, age, gender = GUI()

print('Init script is being executed!!\n')
time.sleep(2)

##Practice or real dataframe?
practice = True if mode =='Practice' else False
##Hints (debug and general idea of the procedure)?
hints = True
if not practice:
    hints = False

dutch = False

monitor = 'jac'  #set 'exp' for experiment, 'jac' for my latitude

# Saving txt after how many trials?
row_save = 5

# After how many trials should we do a break?
#break_num = 60

participants = [0,1,2,3] #list of dataframes we want to create dataframe for each participant


## Randomization controls?
row_check = 10
control_target_cue_match = True
control_same_color = False

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


orientation_target = [0,1] #[90,270] # Only turned down/up
orientation_distractor = [0,1] #[0,180] # Only turned right/left

cue_validity_0 = .76
cue_validity_1 = .83
cue_validity_2 = .9

trials_total = 30 if practice else 630 #Number of rows in the dataframe and of repetitions in the experimental script
series = 1 if practice else 9# Number of series in total - one serie is a set of trials in which cue_identity and cue_validity do NOT change

number_positions = 12  # Search array items
number_distractors = number_positions - 1

colors = [0,1,2]  #['blue','red', 'green']



if keyboard:
    KeyResp = ['down','up']
    esc_keys = ['q', 'escape']
    allowed_keys = KeyResp + esc_keys + ['space']

    headers_answer = 'Reaction_times_Keyboard,Total_trial_time,Items_time,Placeholder_time,Cue_time,is_response_right,response_key,valid_trial'

else:
    KeyResp = [0,6]   #buttons of the cedrus box for response
    allowed_keys = None
    esc_keys = [3]
    headers_answer = 'Reaction_times_Cedrus,Total_trial_time,Items_time,Placeholder_time,Cue_time,is_response_right,Button_pressed,response_key, valid_trial'



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
        print('Gamma configuration file found! Will move it in the right place\n\n')
        shutil.copy(os.path.join(os.getcwd(), gamma_configuration_name), os.path.normpath(gamma_path))
    elif not os.path.isfile(os.path.join(os.getcwd(), gamma_configuration_name)):
        print('Gamma configuration file not found!\n\n')
    elif os.path.isfile(os.path.normpath(os.path.join(gamma_path, gamma_configuration_name))):
        print('Gamma configuration file already present!\n\n')
    mon = monitors.Monitor(name = 'BenQ', width = 53.1, distance = 60)
    mon.setSizePix([1920,1080])
    mon.setCurrent('2019_10_30 16:27_gamma')
elif monitor == 'jac':
    mon = monitors.Monitor('Latitude_Jacopo')
else:
    raise Exception('Monitor name not set correctly!!')
    
    
    
    
### MESSAGES and translation
    
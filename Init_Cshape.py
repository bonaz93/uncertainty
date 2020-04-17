# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 12:18:29 2019

@author: Jacopo

Sets important variables once, for Randomization and experimental script.
Sets implicit or explicit mode, practice or real experiment, language,
response device and participant numbers.
Plus other parameters among which turn on/off some control on randomizations,
possibility to quit the experiment with 'q' or 'esc', monitors...etc
"""

import random
import shutil
import os
import time

from psychopy import monitors

if __name__ != '__main__':
    print('Init script imported...\n')

#Practice or real data_frame/experiment?
practice = False

## Implicit mode?
implicit = True

##Language
dutch = False

## Possible to quit experiment? Must be set to False in real experiment
quiT = True

# Response device: keyboard or Cedrus?
keyboard = True

monitor = 'jac'  #set 'exp' for experiment, 'jac' for my latitude, else 'default'

# Set your working directory (where the scripts are, and where the data is saved)
# wdir = os.getcwd()
wdir = 'C:\\Users\\Jacopo\\OneDrive - Universita degli Studi di Milano-Bicocca\
\\Personal\\Documents\\Universitá\\Psicologia\\AEPS\\Python\\PsychoPy\\Yapf_reformatted'

# Saving txt after how many trials?
row_save = 15

# After how many minutes should we do a break?
break_time = 7  #7 was default

# Creates a dataframe for each participant number
participants = [2]

## Randomization controls?
row_check = 15

if not implicit:
    control_target_cue_match = False  #see Randomization script, needs improvement
    control_same_color = True  #If False, it is possible to have three cues of the same color.

# Set the preferred color space, adjust the labels accordingly.
#To use gammacorrection and isoluminant stimuli, RGB is needed.
#To test on different monitors use HSV.

color_space = 'hsv'

if color_space == 'hsv':
    color_labels = [(240, 1, 1), (0, 1, 1), (90, 1, 1)]
elif color_space == 'rgb':
    color_labels = [
        (-1, -1, 1), (-1 + (255 * 9.6 / 26 * (2 / 255)), -1, -1),
        (-1, -1 + (255 * 9.6 / 79.9 * (2 / 255)), -1)
    ]  #we could use colorspace rgb255 to avoid messing with the ones..
else:
    color_labels = ['blue', 'red', 'green']  # 0, 1, 2

##Hints (debug and general idea of the procedure)?
if not implicit:
    if not practice:
        hints = False
    else:
        hints = True

## CRASH? Edit the line to start again from there in the dataframe
# Need to rename the response dataframe and the info file!!
crash = False
if crash:
    row_crash = 45
else:
    row_crash = 0

orientation_target = [0, 1]  #[90,270] # Only turned down/up
orientation_distractor = [0, 1]  #[0,180] # Only turned right/left

cue_validity_0 = .76
cue_validity_1 = .83
cue_validity_2 = .9

#One serie is a set of trials in which cue_identity and cue_validity do NOT change
series = 1 if practice else 9  # Number of series in total
trials_total = 630  #Number of rows in the dataframe
if practice:
    trials_total = 12 if implicit else 30

number_positions = 12  # Search array items
number_distractors = number_positions - 1

colors = [0, 1, 2]  #['blue','red', 'green']

if keyboard:
    KeyResp = ['down', 'up']
    esc_keys = ['q', 'escape']
    allowed_keys = KeyResp + esc_keys + ['space']
    headers_answer = 'Reaction_times_Keyboard,Total_trial_time,Items_time,Placeholder_time,Cue_time,is_response_right,response_key,valid_trial, cue_identity, cue_validity,\
    color_target, color_cue0, color_cue1, color_cue2'

    if implicit:
        headers_answer = 'Reaction_times_Keyboard,Total_trial_time,Items_time,is_response_right,response_key,valid_trial, cue_identity, cue_validity,\
    color_target'

else:
    KeyResp = [0, 6]  #buttons of the cedrus box for response
    allowed_keys = None
    esc_keys = [3]  #central button of the cedrus
    headers_answer = 'Reaction_times_Cedrus,Total_trial_time,Items_time,Placeholder_time,Cue_time,\
    is_response_right,Button_pressed,response_key, valid_trial, cue_identity, cue_validity,\
    color_target, color_cue0, color_cue1, color_cue2'

    if implicit:
        headers_answer = 'Reaction_times_Cedrus,Total_trial_time,Items_time,\
    is_response_right,Button_pressed,response_key, valid_trial, cue_identity, cue_validity,\
    color_target'

headers = [
    'position_target', 'color_target', 'color_cue0', 'color_cue1',
    'color_cue2', 'ori_target', 'ori_distractor_0', 'ori_distractor_1',
    'ori_distractor_2', 'ori_distractor_3', 'ori_distractor_4',
    'ori_distractor_5', 'ori_distractor_6', 'ori_distractor_7',
    'ori_distractor_8', 'ori_distractor_9', 'ori_distractor_10',
    'ori_distractor_11', 'cue_identity_def', 'cue_validity_def', 'valid_trial',
    'correct_response', 'Start_position'
]
if implicit:
    headers = headers[:2] + headers[5:]

refresh_rate = 60  # in Hertz


def ms_to_frames(ms, rate=refresh_rate):
    return round(ms * rate / 1000)


if practice:
    time_placeholder = range(ms_to_frames(500))
    time_cues = range(ms_to_frames(5000))
    time_fixation = range(
        random.randrange(ms_to_frames(500), ms_to_frames(1000),
                         ms_to_frames(100))
    )  # Random variable must be called everytime inside the script..?
    time_search = 8
    time_iti = range(
        random.randrange(ms_to_frames(500), ms_to_frames(1000),
                         ms_to_frames(100))
    )  # Random variable must be called everytime inside the script..?
else:
    time_placeholder = range(ms_to_frames(500))
    time_cues = range(ms_to_frames(800))
    time_fixation = range(
        random.randrange(ms_to_frames(500), ms_to_frames(1000),
                         ms_to_frames(100))
    )  # Random variable must be called everytime inside the script..?
    time_search = 2.5
    time_iti = range(
        random.randrange(ms_to_frames(500), ms_to_frames(1000),
                         ms_to_frames(100))
    )  # Random variable must be called everytime inside the script..?

if implicit:
    fix_max = 2300
    fix_min = 1800
    time_search = 2.5
else:
    fix_max = 1000
    fix_min = 500

#Inter-trial-interval
iti_max = 1000
iti_min = 500

if implicit:
    # Top button for CEDRUS is 6-----> 6 == YES
    keys_4_answ = ['1', '2', '3'] if keyboard else [0, 3, 6]
    keys_4_answ_reduced = ['1', '3'] if keyboard else [0, 6]

    ### MONITORS.. I can try to laod the json calibration here C:\Users\pp02\AppData\Roaming\psychopy3\monitors
    # Putting the gamma calibration file in the working directory will upload it to the right place in the computer.

gamma_path = 'C:\\Users\\pp02\\AppData\\Roaming\\psychopy3\\monitors\\'
gamma_configuration_name = 'BenQ.json'
if monitor == 'default':
    mon = monitors.Monitor('testMonitor')
elif monitor == 'exp':
    if os.path.isfile(os.path.join(
            os.getcwd(), 'BenQ.json')) and not os.path.isfile(
                os.path.normpath(
                    os.path.join(gamma_path, gamma_configuration_name))):
        print(
            'Gamma configuration file found! Will move it in the right place\n'
        )
        shutil.copy(os.path.join(os.getcwd(), gamma_configuration_name),
                    os.path.normpath(gamma_path))
    elif not os.path.isfile(os.path.join(os.getcwd(),
                                         gamma_configuration_name)):
        print('Gamma configuration file not found!\n')
    elif os.path.isfile(
            os.path.normpath(os.path.join(gamma_path,
                                          gamma_configuration_name))):
        print('Gamma configuration file already present!\n\n')
    time.sleep(2)
    mon = monitors.Monitor(name='BenQ', width=53.1, distance=60)
    mon.setSizePix([1920, 1080])
    mon.setCurrent('2019_10_30 16:27_gamma')
elif monitor == 'jac':
    mon = monitors.Monitor('Latitude_Jacopo')
else:
    raise Exception('Monitor name not set correctly!!')

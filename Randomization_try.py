# -*- coding: utf-8 -*-
"""
Created on Wed Oct 2 15:11:32 2019

@author: Jacopo

This script creates as many dataframes as participants set in the init script,
randomizing the position, color, and orientation of the items.
"""

import math
import os
import time
import numpy as np
import pandas as pd

from Init_Cshape_rev import (trials_total, series, number_positions, colors,
                              orientation_target, orientation_distractor,
                              cue_validity_0, cue_validity_1, cue_validity_2,
                              headers, keyboard, row_check, practice, KeyResp,
                              participants, implicit, wdir)

if not implicit:
    from Init_Cshape_rev import (control_target_cue_match, control_same_color)

if not os.path.isdir(wdir + '\\data'):
    os.mkdir(wdir + '\\data')
    print('created data directory in %s' % wdir)

########################
##     PARAMETERS     ##
########################

if keyboard:
    device_n = 'keyboard'
else:
    device_n = 'Cedrus box'

if not implicit:
    if control_target_cue_match:
        if control_same_color:
            contr = ', controlling for three cues of the same color and cue/target matches every %s rows' % row_check
        else:
            contr = ', controlling only for cue/target matches every %s rows (there will be three cues of the same color)' % row_check
    else:
        if control_same_color:
            contr = ', controlling for three cues of the same color and with pure randomization for the distractor cues.'
        else:
            contr = ' with pure randomization for the distractor cues.'

string = 'Starting...going to build %s dataframes' % (str(len(participants)))\
        + (' for practice' if practice else '')\
        + (contr if not implicit else '')\
        + '\nThe device is %s and the mode is %s' % \
            (device_n, 'implicit\n' if implicit else 'explicit\n')

print(string)

time.sleep(2.5)

############################
##     INITIALIZATION     ##
############################

position_target = np.zeros(trials_total, dtype=int)
start_position = np.zeros(trials_total, dtype=int)
color_target = np.zeros(trials_total, dtype=int)
ori_target = np.zeros(trials_total, dtype=int)
correct_response = np.zeros(trials_total, dtype=int)
if keyboard:
    correct_response = ['na'] * trials_total
cue_identity_def = np.zeros(trials_total, dtype=int)
cue_validity_def = np.zeros(trials_total, dtype=float)
valid_trial = np.zeros(trials_total, dtype=int)
guessed_cues = np.zeros(trials_total, dtype=int)
ori_distractor = np.random.choice(orientation_distractor,
                                  number_positions * trials_total)
if not implicit:
    color_cue0 = np.zeros(trials_total, dtype=int)
    color_cue1 = np.zeros(trials_total, dtype=int)
    color_cue2 = np.zeros(trials_total, dtype=int)
    valid_cue0_def = np.zeros(trials_total, dtype=int)
    valid_cue1_def = np.zeros(trials_total, dtype=int)
    valid_cue2_def = np.zeros(trials_total, dtype=int)

###########################
##     RANDOMIZATION     ##
###########################

# For cycle for creating as many dataframes as participants
for part_num in participants:

    if not os.path.isdir(wdir + '\\data\\part_n_' + str(part_num)):
        os.mkdir(wdir + '\\data\\part_n_' + str(part_num))

    if practice:
        df_name = wdir + '\\data\\part_n_' + str(part_num) + '\\Practice_' + (
            'implicit_' if implicit else '') + str(part_num) + '.csv'
    else:
        df_name = wdir + '\\data\\part_n_' + str(part_num) + '\\Dataframe_' + (
            'implicit_' if implicit else '') + str(part_num) + '.csv'

    if os.path.isfile(df_name):
        iN = input(
            'The dataframe number %s already exists! Press \'y\' to delete it and proceed or \'n\' to cancel (\
 if on Psychopy just stop the script and delete the file because input seems bugged):\n'
            % part_num)
        while not iN in ('y', 'n'):
            iN = input('Please answer \'y\' or \'n\':')
        if iN == 'n':
            raise Exception('CANCELLED')
        os.remove(df_name)
        print('\n\nErased %s and proceeding\n\n' % df_name)

    ### Take care that since lambda is .0125 mean of exp distribution is 80: series and total_trials
#   should be comparable (trials_total%series should not be too high!!), if not the while check for
#   number of trials will go on infinitely.

    if practice:
        cue_switches = np.array(
            [11])  #the identity switch happens in this line during practice
    else:
        tot_trials_check = True
        exp_mean = 70
        lambd = 1 / exp_mean
        #Exponential function copied from Anna's script.
        #Determines the lenght of each series
        while tot_trials_check:
            series_lenght = np.arange(series)
            for switch_ind in series_lenght:
                x = np.random.rand()  #number of random sample
                #inverse transform
                A = math.exp(-40 * lambd) - math.exp(-100 * lambd)
                y = -math.log(math.exp(-40 * lambd) - x * A) / lambd
                series_lenght[switch_ind] = y

            if sum(series_lenght) == (trials_total):
                tot_trials_check = False

        # Array with the trial number in which the switch happens.
        cue_switches = np.delete(np.cumsum(series_lenght), [series - 1])

    if practice:
        cue_validity_all = [.9, .8]
        cue_identity = np.array([0, 1], dtype=int)
    else:
        cue_validity_all = [cue_validity_0, cue_validity_1, cue_validity_2]
        cue_identity = [0, 1, 2]

        # Set all the possible cue identity and cue validity crossing, and shuffle
        arr = []
        for el in cue_validity_all:
            for element in cue_identity:
                arr.append((el, element))

        arr = np.array(arr)
        np.random.shuffle(arr)
        while 0 in np.diff(arr[:, 1]):
            np.random.shuffle(arr)

        cue_validity_all = arr[:, 0]
        cue_identity = np.array(arr[:, 1], dtype=int)

    # For cycle for all the trials - create each row in the dataframe
    for rowI in range(trials_total):

        # Set cue_identity and cue validity, indexing based on how many trials have already been done. Basically changes
        # cue identity and validity when the row corresponds to the switch.
        part = sum(rowI > cue_switches)
        cue_validity_def[rowI] = cue_validity_all[part]
        cue_identity_def[rowI] = cue_identity[part]

        # Set a random position and orientation for the target, set the position in which the drawing starts.
        position_target[rowI] = np.random.choice(number_positions)
        start_position[rowI] = np.random.choice(number_positions)
        ori_target[rowI] = np.random.choice(orientation_target)
        # Set which is the correct answer based on target orientation.
        # CEDRUS BOX response
        if not keyboard:
            if ori_target[rowI] == 0:  #Gap in the bottom
                correct_response[rowI] = KeyResp[0]  #Cedrus button on the left
            else:  #Gap in the top
                correct_response[rowI] = KeyResp[
                    1]  #Cedrus button on the right

        # KEYBOARD response
        else:
            if ori_target[rowI] == 0:
                correct_response[rowI] = 0  #down
            else:
                correct_response[rowI] = 1  # up

        # Number of positions (12) must be perfectly divisible by the number of colors (3)
        if number_positions % len(colors) == 0:
            alfa = int(number_positions / len(colors))

        # Set the weights for the weighted sample of cue colors.
        # First set the weights for the non predictive colors
        weights_distractors = [(1 - cue_validity_def[rowI]) /
                               (len(colors) - 1)] * (len(colors) - 1)

        # Now append the cue_validity to the other colors' weight
        if not implicit:
            weight_predictive_cue = np.append(weights_distractors,
                                              cue_validity_def[rowI])
            color_target[rowI] = np.random.choice(colors)
        else:
            final_weights = np.insert(weights_distractors,
                                      cue_identity_def[rowI],
                                      cue_validity_def[rowI])
            color_target[rowI] = np.random.choice(colors, p=final_weights)

        if not implicit:
            # Adjust(roll) the weights array(which is already right for color_target == 2).
            # If color target == 0, roll weight array of 1 position right
            for roll in range(len(colors) - 1):
                if color_target[rowI] == roll:
                    weight_predictive_cue = np.roll(weight_predictive_cue,
                                                    roll + 1)

            # Set color of cues, the distractor ones at random, the predictive one with weighted sample.
            color_cues = np.random.choice(colors, size=3, replace=True)
            color_cues[cue_identity_def[rowI]] = np.random.choice(
                colors, p=weight_predictive_cue)

            #Control for 3 cues of the same color (only if control is True):
            if control_same_color:
                while color_cues[0] == color_cues[1] == color_cues[2]:
                    color_cues = np.random.choice(colors, size=3, replace=True)
                    color_cues[cue_identity_def[rowI]] = np.random.choice(
                        colors, p=weight_predictive_cue)

            color_cue0[rowI] = color_cues[0]
            color_cue1[rowI] = color_cues[1]
            color_cue2[rowI] = color_cues[2]

        # Determine if the trial is valid or not

        valid_trial[rowI] = 0
        if not implicit:
            if color_target[rowI] == color_cues[cue_identity_def[rowI]]:
                valid_trial[rowI] = 1
        elif color_target[rowI] == cue_identity_def[rowI]:
            valid_trial[rowI] = 1

    # Put every randomized array in a matrix
    objs = (position_target,
            color_target,
            color_cue0,
            color_cue1,
            color_cue2,
            ori_target,
            ori_distractor.reshape((number_positions, trials_total)),
            cue_identity_def,
            cue_validity_def,
            valid_trial,
            correct_response,
            start_position) if not implicit else\
            (position_target,
             color_target,
             ori_target,
             ori_distractor.reshape((number_positions, trials_total)),
             cue_identity_def,
             cue_validity_def,
             valid_trial,
             correct_response,
             start_position)

    matrix = np.transpose(np.vstack(objs))

    #######################################
    ##     CONTROL CUE RANDOMIZATION     ##
    #######################################

    #Not used in real experiment. Code should be rewritten and probabilities calculated
    #accurately after the control is active

    if not implicit:
        if control_target_cue_match:

            full_series = np.append(
                cue_switches, trials_total
            )  # Get the full array of switches and add the final trial

            # For cycle to go through each series/block of cue identity\cue validity
            for start_row, id_I in zip(full_series, range(len(full_series))):

                # Create an array with the adjusted chunk, considering that the rows in a series may not be exactly dividible by [row_check]:
                # So, repeat row_check as many times as possible inside the rows in a series and then add the remainder as last item. EG: if 96 rows and row_check = 10:
                # repeat 10 nine times and append 6: [10,10,10,10,10,10,10,10,10,6]

                temp_serie = np.arange(start_row)
                # Adjust if we are after the first cycle
                if id_I != 0:
                    temp_serie = np.arange(full_series[id_I - 1], start_row)

                # Know the remainder to decide how to split the array
                remainder = len(temp_serie) % row_check

                # if remainder is more than half of the rows I want to check for, split the array one more time
                if remainder > row_check / 2:
                    real_row_check = np.array_split(
                        temp_serie,
                        indices_or_sections=int(len(temp_serie) / row_check) +
                        1)
                else:
                    real_row_check = np.array_split(
                        temp_serie,
                        indices_or_sections=int(len(temp_serie) / row_check))

                # Distractor indexing: choose which are the distractors based on the cue identity (if cue_identity is 1, distractors are [0,1,2] without the 1).
                # Add 2 to match the columns in the matrix and index the real distractors..this is risky because I can mess with the columns indexes
                distr_ind = np.array(
                    [x for x in [0, 1, 2] if x != cue_identity[id_I]]) + 2

                # Inside each series/block, go through each array resulting from the split
                for chunk in real_row_check:

                    # Shuffle the indexing so that rows are randomly accessed
                    np.random.shuffle(chunk)

                    # If color check is not active, we will break the while loop. The things inside the while are
                    # needed to control the cue/target matches anyway
                    same_color_check = True
                    while same_color_check:
                        for distractor in distr_ind:

                            np.random.shuffle(
                                chunk
                            )  # Re-randomize index for every distractor

                            #Iteration for each random row, and keeping the number of repetition to so we can split the chunk in half
                            for rand_row, iteR in zip(chunk,
                                                      range(len(chunk))):

                                if iteR >= int(
                                        len(chunk) / 2
                                ):  # For second half of interval, put distractor color different to the target color
                                    matrix[rand_row,
                                           distractor] = np.random.choice([
                                               x for x in colors
                                               if x != matrix[rand_row, 1]
                                           ])
                                else:
                                    # For the first half of random index interval, put distractor color EQUAL to the target color
                                    matrix[rand_row,
                                           distractor] = matrix[rand_row, 1]

                            # Perform the check of the color only if activated. If not, break.
                            if not control_same_color and distractor == distr_ind[
                                    -1]:
                                same_color_check = False
                                break

                            else:
                                if distractor == distr_ind[
                                        -1]:  # Perform the check only while filling the last distractor.
                                    bool_vect = []
                                    for rand_row in chunk:
                                        # If a row with cue of the same colors is found, stop checking and re-randomize everything.
                                        if matrix[rand_row, 2] == matrix[
                                                rand_row,
                                                3] == matrix[rand_row, 4]:
                                            bool_vect.append(1)
                                            break
                                        else:
                                            bool_vect.append(0)
                                    if sum(bool_vect) == 0:
                                        same_color_check = False

    #this just prints out probabilities to check, beware participants do not see this!!
    else:  #implicit task
        if not practice:
            for i in set(matrix[:, -5]):
                matrix_id = matrix[matrix[:, -5] == i]
                frequency_id = round(
                    len(matrix_id[matrix_id[:, 1] == i]) / len(matrix_id) *
                    100, 2)
                print(
                    '\nFrequency of color %s where cue_identity is %s is %s%%\n'
                    % (i, i, frequency_id))
            print('\nCue identity levels: {}\n\n'.format(cue_validity_all))

################################################################
##     CHECK FREQUENCIES FOR DISTRACTOR CUE RANDOMIZATION     ##
################################################################

#Uncomment the prints below to show!

    if not implicit:
        c0_id0 = 0
        c0_id1 = 0
        c0_id2 = 0

        c1_id0 = 0
        c1_id1 = 0
        c2_id2 = 0

        c2_id0 = 0
        c2_id1 = 0
        c1_id2 = 0

        tot_id0 = 0
        tot_id1 = 0
        tot_id2 = 0
        same_col_cues = 0

        diff_3_cues = 0
        diff_2_cues = 0

        for i in range(len(matrix)):
            #        if matrix[i,2] == matrix[i,3] == matrix[i,4]:
            #            same_col_cues += 1

            if matrix[i, -5] == 0:
                tot_id0 += 1
                if matrix[i, 3] == matrix[i, 1]:
                    c1_id0 += 1
                if matrix[i, 4] == matrix[i, 1]:
                    c2_id0 += 1
                if matrix[i, 2] == matrix[i, 1]:
                    c0_id0 += 1

            if matrix[i, -5] == 1:
                tot_id1 += 1
                if matrix[i, 2] == matrix[i, 1]:
                    c0_id1 += 1
                if matrix[i, 4] == matrix[i, 1]:
                    c2_id1 += 1
                if matrix[i, 3] == matrix[i, 1]:
                    c1_id1 += 1

            if matrix[i, -5] == 2:
                tot_id2 += 1
                if matrix[i, 2] == matrix[i, 1]:
                    c0_id2 += 1
                if matrix[i, 3] == matrix[i, 1]:
                    c1_id2 += 1
                if matrix[i, 4] == matrix[i, 1]:
                    c2_id2 += 1

            if len(set(matrix[i, 2:5])) == 3:
                diff_3_cues += 1
            elif len(set(matrix[i, 2:5])) == 2:
                diff_2_cues += 1
            else:
                same_col_cues += 1

        same_col_cue_percentage = round(same_col_cues / trials_total * 100, 1)
        diff_3_cues_percentage = round(diff_3_cues / trials_total * 100, 1)
        diff_2_cues_percentage = round(diff_2_cues / trials_total * 100, 1)

        cue_0_mean = round(np.mean(color_cue0), 2)
        cue_1_mean = round(np.mean(color_cue1), 2)
        cue_2_mean = round(np.mean(color_cue2), 2)
        color_target_mean = round(np.mean(color_target), 2)

        print('\n\nDataframe %s:\
            \nTimes distractors are equal to color target when cue id = 0: c1 = %s%% and c2 = %s%% on total of %s (predictive cue: %s%%)\
            \nTimes distractors are equal to color target when cue id = 1: c0 = %s%% and c2 = %s%% on total of %s (predictive cue: %s%%)\
            \nTimes distractors are equal to color target when cue id = 2: c0 = %s%% and c1 = %s%% on total of %s (predictive cue: %s%%)\n\n\
        mean color cue0 = %s,   mean color cue1 = %s,   mean color cue2 = %s, mean color target = %s\n\n\
        Trials with 3 different cues = %s%%\n\
        Trials with 2 cues of the same color = %s%%\n\
        Trials with three cues of the same color: %s (percentage = %s%%)\n\n\
        ' % (part_num, c1_id0 * 100 // tot_id0, c2_id0 * 100 // tot_id0,
             tot_id0, c0_id0 * 100 // tot_id0, c0_id1 * 100 // tot_id1,
             c2_id1 * 100 // tot_id1, tot_id1, c1_id1 * 100 // tot_id1,
             c0_id2 * 100 // tot_id2, c1_id2 * 100 // tot_id2, tot_id2,
             c2_id2 * 100 // tot_id2, cue_0_mean, cue_1_mean, cue_2_mean,
             color_target_mean, diff_3_cues_percentage, diff_2_cues_percentage,
             same_col_cues, same_col_cue_percentage))

    #################################
    ##     EXPORT TO DATAFRAME     ##
    #################################

    df = pd.DataFrame(matrix, columns=headers)

    if practice:
        df.to_csv(path_or_buf=df_name)
        print('Practice dataframe %s exported in %s\n' % (part_num, df_name))
    else:
        df.to_csv(path_or_buf=df_name)
        print('Dataframe %s exported in %s\n' % (part_num, df_name))
    time.sleep(.5)

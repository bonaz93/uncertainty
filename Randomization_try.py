# -*- coding: utf-8 -*-
"""
Created on Wed Oct 2 15:11:32 2019

@author: Jacopo

This script creates as many dataframes as participants, randomizing the position, color, and orientation of the items
A controlled randomization is done on cue colors where matches with the color target are checked to be exaclty half of the
lines checked; having three cues of the same color is nalso avoided."""


import numpy as np, pandas as pd, math, os, time

wdir = os.getcwd()

########################
##     PARAMETERS     ##
########################



if not os.path.isdir(wdir + '\\data'):
    os.mkdir(wdir + '\\data')



from Init_Cshape import trials_total, series, number_positions, colors,\
orientation_target,orientation_distractor,cue_validity_0,cue_validity_1,\
cue_validity_2, headers, keyboard, control_target_cue_match, control_same_color, row_check, practice, KeyResp,\
participants


if keyboard:
    device_n = 'keyboard'
else:
    device_n = 'Cedrus box'

if control_target_cue_match:
    if control_same_color:
        contr = 'controlling for cues of the same color and cue/target matches every %s rows'%row_check
    else:
        contr = 'controlling only for cue/target matches every %s rows (there will be three cues of the same color)'%row_check
else:
    contr = 'with pure randomization for the distractor cues.'


if practice:
    string = 'Starting...going to build %s dataframes for PRACTICE '%(participants) + contr + '\nThe device is ' + device_n + '\n\n'
else:
    string = 'Starting...going to build %s dataframes '%(participants) + contr + '\nThe device is ' + device_n + '\n\n'

print(string)

time.sleep(1)

############################
##     INITIALIZATION     ##
############################


position_target = np.zeros(trials_total, dtype = int)
start_position = np.zeros(trials_total, dtype = int)
color_target = np.zeros(trials_total, dtype = int)
ori_target = np.zeros(trials_total, dtype = int)
color_cue0 = np.zeros(trials_total, dtype = int)
color_cue1 = np.zeros(trials_total, dtype = int)
color_cue2 = np.zeros(trials_total, dtype = int)
correct_response = np.zeros(trials_total, dtype = int)
if keyboard:
    correct_response = ['na']*trials_total
cue_identity_def = np.zeros(trials_total, dtype = int)
cue_validity_def = np.zeros(trials_total, dtype = float)
valid_cue0_def = np.zeros(trials_total, dtype = int)
valid_cue1_def = np.zeros(trials_total, dtype = int)
valid_cue2_def = np.zeros(trials_total, dtype = int)
valid_trial = np.zeros(trials_total, dtype = int)
guessed_cues = np.zeros(trials_total, dtype = int)
ori_distractor = np.random.choice(orientation_distractor, number_positions*trials_total)


###########################
##     RANDOMIZATION     ##
###########################

# For cycle for creating as many dataframes as participants
for part_num in participants:
    
    if not os.path.isdir(wdir + '\\data\\part_n_' + str(part_num)):
        os.mkdir(wdir + '\\data\\part_n_' + str(part_num))


    if practice:
        df_name = wdir + '\\data\\part_n_' + str(part_num) + '\\Practice_' + str(part_num) + '.csv'
    else:
        df_name = wdir + '\\data\\part_n_' + str(part_num) + '\\Dataframe_' + str(part_num) + '.csv'

    if os.path.isfile(df_name):
        iN = input('The dataframe number %s already exists! Press \'y\' to delete it and proceed or \'n\' to cancel:\n'%part_num)
        while not iN in ['n','y']:
            iN = input('Please answer \'y\' or \'n\':')
            if iN == 'y' or iN == 'n':
                break
        if iN == 'n':
            raise Exception('CANCELLED')
        else:
            os.remove(df_name)
            print('\n\nErased %s and proceeding\n\n'%df_name)


    ### Take care that since lambda is .0125 mean of exp distribution is 80: series and total_trials
#   should be comparable (trials_total%series should not be too high!!), if not the while check for
#   number of trials will go on infinitely.
    
    if practice:
        cue_switches = np.array([11])

    else:
        tot_trials_check = True
    
        exp_mean = 70
        lambd = 1/exp_mean
        
        while tot_trials_check:
            series_lenght = np.arange(series)
            for switch_ind in series_lenght:
                x = np.random.rand()#                       number of random sample
                A = math.exp(-40*lambd)-math.exp(-100*lambd)#;         % inverse transform
                y = -math.log(math.exp(-40*lambd) - x*A) / lambd #;       % inverse transform
                series_lenght[switch_ind] = y
    
            if sum(series_lenght) == (trials_total):
                tot_trials_check = False
    
        # Array with the trial number in which the switch happens.
        cue_switches = np.delete(np.cumsum(series_lenght),[series-1])



    if practice:
        cue_validity_all = [.9,.8]
        cue_identity = np.array([0,1], dtype = int)
    else:
        cue_validity_all = [cue_validity_0, cue_validity_1, cue_validity_2]
        cue_identity = [0,1,2]
    
        # Set all the possible cue identity and cue validity crossing, and shuffle
        arr = []
        for el in cue_validity_all:
            for element in cue_identity:
                arr.append((el,element))
    
        arr = np.array(arr)
        np.random.shuffle(arr)
    
        while 0 in np.diff(arr[:,1]):
            np.random.shuffle(arr)
    
        cue_validity_all = arr[:,0]
        cue_identity = np.array(arr[:,1], dtype = int)




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
                if ori_target[rowI] == 0:        #Gap in the bottom
                    correct_response[rowI] = KeyResp[0]   #Cedrus button on the left
                else:                            #Gap in the top
                    correct_response[rowI] = KeyResp[1]   #Cedrus button on the right

        # KEYBOARD response
        else:
            if ori_target[rowI] == 0:
                correct_response[rowI] = 0 #down
            else:
                correct_response[rowI] = 1 # up


        # Number of positions (12) must be perfectly divisible by the number of colors (3)
        if number_positions%len(colors) == 0:
            alfa = int(number_positions/len(colors))

        # Determine target color: eg if target position is lower than 3, the color is blue. This is because of how the 
        # drawing of the search array is done in the other script: always starts with 4 blue, then 4 red, the 4 green.
        color_target[rowI] = colors[0] if position_target[rowI] < alfa else (colors[2] if position_target[rowI] >= (number_positions-alfa) else colors[1])


        # Set the weights for the weighted sample of cue colors.
        # First set the weights for the non predictive colors
        weights_distractor_cues = [(1-cue_validity_def[rowI])/(len(colors) - 1)] * (len(colors) - 1)

        # Now append the cue_validity to the other colors' weight
        weight_predictive_cue = np.append(weights_distractor_cues, cue_validity_def[rowI])

        # Adjust(roll) the weights array(which is already right for color_target == 2).
        # If color target == 0, roll weight array of 1 position right
        for roll in range(len(colors) - 1):
            if color_target[rowI] == roll:
                weight_predictive_cue = np.roll(weight_predictive_cue, roll+1)

        # Set color of cues, the distractor ones at random, the predictive one with weighted sample.
        color_cues = np.random.choice(colors, size = 3, replace = True)
        color_cues[cue_identity_def[rowI]] = np.random.choice(colors, p = weight_predictive_cue)

        #Control for 3 cues of the same color (only if control is True):
        if control_same_color:
            while np.diff(color_cues, 2) == 0:
                color_cues = np.random.choice(colors, size = 3, replace = True)
                color_cues[cue_identity_def[rowI]] = np.random.choice(colors, p = weight_predictive_cue)

        color_cue0[rowI] = color_cues[0]
        color_cue1[rowI] = color_cues[1]
        color_cue2[rowI] = color_cues[2]

        # Determine if the trial is valid or not
        if color_target[rowI] == color_cues[cue_identity_def[rowI]]:
            valid_trial[rowI] = 1
        else:
            valid_trial[rowI] = 0


    # Put every randomized array in a matrix
    matrix = np.transpose(np.vstack((position_target, color_target, color_cue0, color_cue1, color_cue2, ori_target,
                                     ori_distractor.reshape((number_positions,trials_total)), cue_identity_def,
                                     cue_validity_def, valid_trial, correct_response, start_position)))



    #######################################
    ##     CONTROL CUE RANDOMIZATION     ##
    #######################################

    # Only if control is True
    if control_target_cue_match:

        full_series = np.append(cue_switches, trials_total)  # Get the full array of switches and add the final trial

        # For cycle to go through each series/block of cue identity\cue validity
        for start_row,id_I in zip(full_series,range(len(full_series))):
        
            # Create an array with the adjusted chunk, considering that the rows in a series may not be exactly dividible by [row_check]:
            # So, repeat row_check as many times as possible inside the rows in a series and then add the remainder as last item. EG: if 96 rows and row_check = 10:
            # repeat 10 nine times and append 6: [10,10,10,10,10,10,10,10,10,6]


            temp_serie = np.arange(start_row)
            # Adjust if we are after the first cycle
            if id_I != 0:
                temp_serie = np.arange(full_series[id_I - 1],start_row)

            # Know the remainder to decide how to split the array
            remainder = len(temp_serie) % row_check

            # if remainder is more than half of the rows I want to check for, split the array one more time
            if remainder > row_check/2:
                real_row_check = np.array_split(temp_serie, indices_or_sections = int(len(temp_serie) / row_check) + 1)
            else:
                real_row_check = np.array_split(temp_serie, indices_or_sections = int(len(temp_serie) / row_check))


            # Distractor indexing: choose which are the distractors based on the cue identity (if cue_identity is 1, distractors are [0,1,2] without the 1).
            # Add 2 to match the columns in the matrix and index the real distractors..this is risky because I can mess with the columns indexes
            distr_ind = np.array([x for x in [0,1,2] if x != cue_identity[id_I]]) + 2


            # Inside each series/block, go through each array resulting from the split
            for chunk in real_row_check:

                # Shuffle the indexing so that rows are randomly accessed
                np.random.shuffle(chunk)

                # If color check is not active, we will break the while loop. The things inside the while are 
                # needed to control the cue/target matches anyway
                same_color_check = True
                while same_color_check:
                    for distractor in distr_ind:

                        np.random.shuffle(chunk) # Re-randomize index for every distractor

                        #Iteration for each random row, and keeping the number of repetition to so we can split the chunk in half
                        for rand_row, iteR in zip(chunk, range(len(chunk))):
    
                            if iteR >= int(len(chunk)/2):  # For second half of interval, put distractor color different to the target color
                                matrix[rand_row,distractor] = np.random.choice([x for x in colors if x != matrix[rand_row,1]])
                            else:
                                # For the first half of random index interval, put distractor color EQUAL to the target color
                                matrix[rand_row,distractor] = matrix[rand_row,1]

                        # Perform the check of the color only if activated. If not, break.
                        if not control_same_color and distractor == distr_ind[-1]:
                            same_color_check = False
                            break

                        else:
                            if distractor == distr_ind[-1]:  # Perform the check only while filling the last distractor.
                                bool_vect = []
                                for rand_row in chunk:
                                    # If a row with cue of the same colors is found, stop checking and re-randomize everything.
                                    if np.diff(matrix[rand_row,2:5],2) == 0:
                                        bool_vect.append(1)
                                        break
                                    else:
                                        bool_vect.append(0)
                                if sum(bool_vect) == 0:
                                    same_color_check = False


#                for rand_row in chunk:
#                    matrix[rand_row,[distr_ind]] = np.random.choice([x for x in colors if x != matrix[rand_row,1]])
#                    matrix[rand_row,[distr_ind]] = matrix[rand_row,1]
#
#                print('shuffling this chunk %s from %s to %s'%(chunk, chunk[0], chunk[-1]))
#                print('original array:', matrix[chunk[0]:chunk[-1], distr_ind[0]])
#                print('original matrix:\n', matrix[chunk, 1:5])
#                np.random.shuffle(matrix[chunk[0]:chunk[-1], distr_ind[0]])
#                np.random.shuffle(matrix[chunk[0]:chunk[-1], distr_ind[1]])
#                print('shufled array:', matrix[chunk[0]:chunk[-1], distr_ind[0]])
#                print('matrix shuffled:\n', matrix[chunk, 1:5])
#
#                same_color_check = True if control_same_color else False
#                while same_color_check:
#                    np.random.shuffle(matrix[chunk[0]:chunk[-1], distr_ind[0]])
#                    np.random.shuffle(matrix[chunk[0]:chunk[-1], distr_ind[1]])
#
#                    bool_vect = []
#                    for rand_row in chunk:
#                        if np.diff(matrix[rand_row,2:5],2) == 0:
#                            bool_vect.append(1)
#                            break
#                    if sum(bool_vect) == 0:
#                        same_color_check = False


    ################################################################
    ##     CHECK FREQUENCIES FOR DISTRACTOR CUE RANDOMIZATION     ##
    ################################################################
    
    
    c1_id0 = 0
    c2_id0 = 0
    c0_id1 = 0
    c2_id1 = 0
    c0_id2 = 0
    c1_id2 = 0
    tot_id0 = 0
    tot_id1 = 0
    tot_id2 = 0
    same_col_cues = 0

    for i in range(len(matrix)):
        if matrix[i,2] == matrix[i,3] == matrix[i,4]:
            same_col_cues += 1

        if matrix[i,-5] == 0:
            tot_id0 += 1
            if matrix[i,3] == matrix[i,1]:
                c1_id0 += 1
            if matrix[i,4] == matrix[i,1]:
                c2_id0 +=1
        
        
        if matrix[i,-5] == 1:
            tot_id1 += 1
            if matrix[i,2] == matrix[i,1]:
                c0_id1 += 1
            if matrix[i,4] == matrix[i,1]:
                c2_id1 +=1
        
        if matrix[i,-5] == 2:
            tot_id2 += 1
            if matrix[i,2] == matrix[i,1]:
                c0_id2 += 1
            if matrix[i,3] == matrix[i,1]:
                c1_id2 +=1



    print('Dataframe %s:\
    \nTrials with three cues of the same color: %s\
    \nTimes distractors are equal to color target when cue id = 0: c1 = %s and c2 = %s on total of %s\
    \nTimes distractors are equal to color target when cue id = 1: c0 = %s and c2 = %s on total of %s\
    \nTimes distractors are equal to color target when cue id = 2: c0 = %s and c1 = %s on total of %s\n'%(part_num,same_col_cues,c1_id0,c2_id0,tot_id0,c0_id1,c2_id1,tot_id1,c0_id2,c1_id2,tot_id2))
    
    
    
    
    
    
    #################################
    ##     EXPORT TO DATAFRAME     ##
    #################################
    
    
    
    df = pd.DataFrame(matrix, columns = headers)
    
    #crosstab1 = pd.crosstab([color_cue0,color_cue1,color_cue2,color_target],cue_identity_def,colnames=['cue identity'], rownames= ['color cue 0','color cue 1','color cue 2','target color'], margins=True)
    #crosstab2 = pd.crosstab(cue_validity_def,cue_identity_def,rownames=['validity'],colnames=['identity'], margins = True, normalize = True)
    
    #sns.heatmap(crosstab1)

    if practice:
        df.to_csv(path_or_buf = df_name)
        print('Practice dataframe %s exported in %s\n\n\n'%(part_num,df_name))
    else:
        df.to_csv(path_or_buf = df_name)
        print('Dataframe %s exported in %s\n\n\n'%(part_num,df_name))

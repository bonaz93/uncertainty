# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 13:14:14 2019

@author: Jacopo
"""

""" 
Goodmorning everyone, 

On Monday I will start piloting the experiment and on Friday the first participants will be tested. I will try to explain briefly the script(s)
and to show you how to control some options so that you can try it and check the procedure if you like.

The script called 'Randomization_Cshape' builds the dataframes with the data needed by the experimental script. Here the colors, positions and orientation
of the items is randomized (and optionally controlled in some ways), the validity of a trial and the correct response are coded, the cue identity and validity are set.

Many variables are imported from the script 'init_exp', such as the number of trials, the number of blocks, the cue identity and validity levels. Also the 
different timings are set at the end of this script.
Importantly, some options (boolean variables) are devised to control some features:
    - Whether or not to show the hints (line 41)
    - If it is possible to quit the experiment (press Q or esc in the search phase - line 49)
    - Which is the response device (Cedrus box or keyboard - line 52)
    - Which controls are performed on the randomization of the cue colors (line 45 and 46). If the first variable control_target_cue_match is set to false, NO control is performed;
      if control_same_color is set to True (only makes sense if also the first variable is True) then having three cue of the same color is avoided in any trial.
      
      So basically there are paths the script can take:
          - control_target_cue_match = False  In this case, the randomization is pure: the distractors cues are chosen totally randomly.
          - control_target_cue_match = True and control_same_color = False  In this case, the number of times a distractor matches the color of the target is controlled. 
            You can set on how many rows this check is done in line 44 (row_check). Now on every 16 rows we are forcing both distractors to match the color of the target 8 times,
            and to not match the color of the target the other 8 times.
          - Both controls True. Same as previous option but having three cues of the same color is avoided. Don't put row_check > 18 otherwise it will take ages to complete
            because of poor implementation (basically I try to randomize again whenever three cues are of the same colors, and this happens pretty often).
            
The Cshape_functions script just defines some functions for the GUI, the response with the Cedrus and the Instructions.

The Cshape script imports the dataframe create before and does the drawing and response collection. The data is then saved in a txt (which is also created every X trials - how many is set in the init script)
This is the "real" experiment, or at least the code that does the dirty work and that uses psychopy.



**Instructions for use**

Put the scripts in one folder and set it as working directory
Set your preferences in init script: specify if you want to build a datafram for practice or for the real experiment (line 14). Also decide how many dataframes to create setting the number of participants in the randomization script(one for practice and one for the experiment?).
Launch the randomization script (once for practice, once for real experiment), it will create dataframes in ~working_directory/data
Set in init script practice True or False
Launch the Cshape script: when prompted, insert the participant number and choose between experiment or practice. **NOTE that this number will determine which dataframe is used to build the stimuli (eg, dataframe 0 for participant number 0)
The data collected is saved in a txt in the data folder.
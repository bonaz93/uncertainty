# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:22:04 2020

@author: Jacopo
"""

from Init_Cshape_rev import dutch, keyboard, implicit

### MESSAGES and translation: creates a dictionary with all needed messages
### 3 main parameters for difference in messages: task (implicit/explicit),
### language and device(keyboards vs cedrus)

message_dict = dict()

if keyboard:
    wrong_key_text = 'Wrong button, please only respond with up or down arrow' if not dutch else\
    'Verkeerde knop, reageer alsjeblieft alleen met de bovenste of de onderste toets'
    buttoN = 'the spacebar' if not dutch else 'de spatiebalk'

else:
    wrong_key_text = 'Wrong button, please only respond with the first and last button' if not dutch else\
    'Verkeerde knop, reageer alsjeblieft alleen met de bovenste of de onderste toets'
    buttoN = 'a button' if not dutch else 'de responsknop'

if not implicit:  #EXPLICIT TASK
    switch_text = 'The position of the predictive cue is about to change!' if not dutch else 'De positie van de voorspellende cue gaat bijna veranderen!'
    no_more_mess_text = 'No more hints! Can you follow the right cue?' if not dutch else 'Geen hints meer! Kun je de juiste cue volgen?'
    hint_text = 'The reliable cue is in the {} position' if not dutch else 'De betrouwbare cue staat in de {} positie'
    important_message_remember = 'Always try to understand which of the three cues is the reliable one (more often colored as the target) and use it to find the target faster!\n\n\
     And remember that:\
    \n\n\n - The reliable cue will not *always* be of the same color of the target, but *most of the times* it will!\
    \n\n\n - The reliable cue can change position after a certain amount of trials' if not dutch else\
    'Probeer te begrijpen welke van de drie signalen de betrouwbare is (vaker gekleurd als het doelwit) en gebruik het om\
 het doel sneller te vinden!\n\n\
     En onthoud dat:\
    \n\n\n - De betrouwbare cue zal niet *altijd* van dezelfde kleur zijn als het doelwit, maar *meestal* wel!\
    \n\n\n - De betrouwbare cue zal van positie veranderen na een variabel aantal trials.'

    invalid_hint = 'This trial was invalid! The reliable cue was not of the same color of the target, but this doesn\'t necessarly mean\
 that it switched position!' if not dutch else\
    'Deze trial was ongeldig! De betrouwbare cue was niet van dezelfde kleur als het doelwit, \
 maar dit betekent niet noodzakelijkerwijs dat het van plaats veranderd is!'

    end_practice = 'Good job! As you may have noticed, very often but not always the reliable cue has the same \
color of the target!\n\nIn the real experiment you will have no hints and you will need to infer when the reliable\
 cue has changed position to make a good performance :)' if not dutch else 'Goed zo! Zoals je misschien gemerkt hebt heeft de\
 betrouwbare cue vaak, maar niet altijd, dezelfde kleur als de target! In het echte experiment heb je geen hints en moet je raden\
 wanneer de betrouwbare cue van positie is veranderd om een goede prestatie te leveren :)'

    message_2_target = 'Please look at the fixation point in the center of the screen and start your search from there!\nThe target will be always present and you have to respond to its orientation in this way:\
    \n\n- Press the button on the top with your {} index finger if the gap is on the top of the shape.\
    \n- Press the button on the bottom with your {} index finger if the gap is on the bottom of the shape.' if not dutch else\
    'Kijk naar het fixatiekruis in het midden van het scherm tot de stimuli op het scherm verschijnen, begin dan onmiddellijk met zoeken!\
 Er zal altijd een target aanwezig zijn en je moet reageren op de oriëntatie van deze target:\
    \n\n- Duw met je {} wijsvinger op de bovenste toets als de opening aan de bovenkant is.\
    \n- Duw met je {} wijsvinger op de onderste toets als de opening aan de onderkant is.'


    message_3_cues = 'Before the search, a set of 3 colored cues will appear (colors will change every trial). Please note that:\
    \n\n- Only ONE of the 3 cues will often have the same color of the target, helping you in the visual search!\
    \n\n- The other 2 cues will be colored randomly.' if not dutch else\
    'Voor de zoektaak begint zal een set van 3 gekleurde cues verschijnen (kleuren veranderen van trial tot trial). Let op dat:\
    \n\n\n- Enkel ÉÉN van de 3 cues een correct voorspellende cue is, en enkel deze cue heeft hetzelfde kleur als de target. Dit kan je helpen in de visuele zoektaak.\
    \n\n- De andere 2 cues zullen een willekeurige kleur hebben.'


    message_objective = '**You also have to guess which of the three cues is the one that is OFTEN colored as the target in order to make a quick detection!**'if not dutch else\
    '**Je zal moeten raden welk van de 3 cues de correct voorspellende cue is. Dus, welke cue VAAK hetzelfde kleur heeft als de target om zo de target snel te kunnen detecteren.**'

    message_4_switch = 'The cue often colored as the target will not remain the same for the whole experiment (for example, it can switch \
from the right position to the top one after some trials). Generally, this cue change will happen a few times within the experiment (but note that it won\'t change too often - NOT every few trials...' if not dutch else\
    'Welke cue vaak dezelfde kleur heeft als de target, zal niet gedurende het hele experiment hetzelfde blijven (het kan bijvoorbeeld na \
 enkele trials veranderen van de rechter positie naar de bovenste positie). Over het algemeen zal deze cue verandering een paar\
 keer binnen elk blok gebeuren (maar let op: het zal niet te vaak veranderen).'


    recap_message = 'Just a few things before we get started:\n\n\n\
    - Remember to use the reliable cue to speed up the visual search (respond as fast and as accurately as possible)\n\n\
    - Try to notice if the cue you are using is reliable or not\n\n\
    - Always look at the fixation cross in the center before the search!' if not dutch else\
    'Een paar dingen voordat we beginnen:\n\n\n\
    - Vergeet niet de betrouwbare cue te gebruiken om het visueel zoeken te versnellen (reageer zo snel en zo accuraat mogelijk).\n\n\
    - Probeer op te merken of de cue die je gebruikt betrouwbaar is of niet.\n\n\
    - Kijk altijd naar het fixatiekruis in het midden voor het zoeken!'

    message_dict.update(switch_text=switch_text,
                        no_more_mess_text=no_more_mess_text,
                        hint_text=hint_text,
                        important_message_remember=important_message_remember,
                        invalid_hint=invalid_hint,
                        message_3_cues=message_3_cues,
                        message_objective=message_objective,
                        message_4_switch=message_4_switch)

else:  #IMPLICIT TASK
    message_2_target = 'Please look at the fixation point in the center of the screen and start your search from there!\nThe\
 target will be always present and you have to respond to its orientation in this way:\
    \n\n\n- Press the button on the top with your {} index finger if the gap is on the top of the shape.\
    \n\n- Press the button on the bottom with your {} index finger if the gap is on the bottom of the shape.' if not dutch else\
    'Kijk naar het fixatiekruis in het midden van het scherm tot de stimuli op het scherm verschijnen, begin dan onmiddellijk met zoeken!\
 Er zal altijd een target aanwezig zijn en je moet reageren op de oriëntatie van deze target:\
    \n\n- Duw met je {} wijsvinger op de bovenste toets als de opening aan de bovenkant is.\
    \n\n- Duw met je {} wijsvinger op de onderste toets als de opening aan de onderkant is.'

    recap_message = 'Just a few things before we get started:\n\n\n\
    \n\n- Press the button on the top with your {} index finger if the gap is on the top of the shape.\
    \n- Press the button on the bottom with your {} index finger if the gap is on the bottom of the shape.\
    \n- Always look at the fixation cross in the center before the search!' if not dutch else\
    'Een paar dingen voordat we beginnen:\n\
    \n\n- Duw met je {} wijsvinger op de bovenste toets als de opening aan de bovenkant is.\
    \n\n- Duw met je {} wijsvinger op de onderste toets als de opening aan de onderkant is.\
    \n\n- Kijk altijd naar het fixatiekruis in het midden voor het zoeken!'

    end_practice = 'Good job!' if not dutch else 'Goed zo!'

    questions_text = 'The task is over! Please answer a few questions about the color of the target :)' if not dutch else\
    'De taak is voorbij! Beantwoord a.u.b. een paar vragen over de kleur van het doelwit :)'

    Q0_text = 'Did you notice any regularities regarding the color of the target? Please press the top button for ‘yes’ and the bottom button for ‘no’'\
    if not dutch else 'Heeft u enige regelmatigheden opgemerkt met betrekking tot de kleur van het doelwit?\
 Druk op de bovenste knop voor \'ja\' en de onderste knop voor \'nee\''

    Q1_text = 'Was the target often colored with one specific color throughout the whole experiment? Please press the top button for ‘yes’ and the bottom button for ‘no’'\
    if not dutch else 'Was het doelwit vaak één specifieke kleur gedurende het hele experiment?\
 Druk op de bovenste knop voor ’ja’ en de onderste knop voor ’nee’'

    Q1_0_text = 'Which color do you think the target was most often colored with? Please press the top button for ‘red’, the middle button for ‘blue’ and the bottom button for ‘green’'\
    if not dutch else 'Welke kleur denk je dat het doelwit het meest gekleurd was? Druk op de bovenste knop voor ’rood’,\
 de middelste knop voor ’blauw’ en de onderste knop voor ’groen’'

    Q2_text = 'Did you notice that the most probable color of the target was changing during the experiment\
 (for example, in one part it was blue, and then red, and then green)? Press the top button for ‘yes’ and the bottom button for ‘no’' if not dutch else\
 'Merkte je dat de meest waarschijnlijke kleur van het doelwit tijdens het experiment veranderde\
 (bijvoorbeeld, in één deel was het blauw, en dan rood, en dan groen)?\
 Druk op de bovenste knop voor ’ja’ en de onderste knop voor ’nee’'

    Q2_0_text = 'How many times do you think the most probable color of the target has changed throughout the experiment? Please press the top button\
 if you think it changed around 3 times, the middle button if it changed around 8 times and the top button if it changed around 13'\
    if not dutch else 'Hoe vaak denk je dat de meest waarschijnlijke kleur van het doelwit tijdens het experiment is veranderd?\
 Druk op de bovenste knop als u denkt dat de kleur ongeveer 4 keer is veranderd, de middelste knop als deze ongeveer 9 keer is veranderd en de bovenste knop als deze ongeveer 14 keer is veranderd.'

    wrong_answer_text = 'Wrong button, please only respond with the indicated buttons' if not dutch else\
    'Verkeerde knop, reageer alleen met de aangegeven knoppen.'

    keys_4_answ = ['1', '2', '3'] if keyboard else [
        0, 3, 6
    ]  # Top button for CEDRUS is 6-----> 6 == YES
    keys_4_answ_reduced = ['1', '3'] if keyboard else [0, 6]

    message_dict.update(questions_text=questions_text,
                        Q0_text=Q0_text,
                        Q1_text=Q1_text,
                        Q1_0_text=Q1_0_text,
                        Q2_text=Q2_text,
                        Q2_0_text=Q2_0_text,
                        wrong_answer_text=wrong_answer_text,
                        keys_4_answ=keys_4_answ,
                        keys_4_answ_reduced=keys_4_answ_reduced)

space = 'Press {} to continue...' if not dutch else 'druk op {} om verder te gaan...'

message_1_welcome = 'Welcome to the experiment, {0}! In this visual search task, you are asked to detect as quickly\
 and accurately as possible one target among distractors.\n\nAll the items are shapes of 3 different random colors (red, blue or green - changing randomly),\
 with a gap on one side:\
\n\n- Target items have a gap on either the upper or the lower part.\
\n- Distractors have a gap on the left or on the right.' if not dutch else\
'Welkom in dit experiment, {0}! In deze visuele zoektaak zal je zo snel\
 en accuraat mogelijk een target moeten detecteren tussen distractoren (afleiders). Deze stimuli zijn vormen in 3 verschillende kleuren (rood, blauw of groen) met een opening aan één kant:\
\n\n- Target stimuli hebben ofwel aan de bovenkant ofwel aan de onderkant een opening\
\n- Distractoren hebben ofwel aan de linkerkant ofwel aan de rechterkant een opening.'

message_2_target = 'Please look at the fixation point in the center of the screen and start your search from there!\nThe\
 target will be always present and you have to respond to its orientation in this way:\
\n\n\n- Press the button on the top with your {} index finger if the gap is on the top of the shape.\
\n\n- Press the button on the bottom with your {} index finger if the gap is on the bottom of the shape.' if not dutch else\
'Kijk naar het fixatiekruis in het midden van het scherm tot de stimuli op het scherm verschijnen, begin dan onmiddellijk met zoeken!\
 Er zal altijd een target aanwezig zijn en je moet reageren op de oriëntatie van deze target:\
\n\n- Duw met je {} wijsvinger op de bovenste toets als de opening aan de bovenkant is.\
\n\n- Duw met je {} wijsvinger op de onderste toets als de opening aan de onderkant is.'

message_5_questions = 'Please ask any question now if something is not clear!' if not dutch else\
'Is alles duidelijk? Zo niet, stel alsjeblieft vragen aan de proefleider!'

message_6 = 'You will start with some practice trials as soon as you press a button..' if not dutch else\
'Druk op een knop om te beginnen met enkele oefentrials.'

message_final = 'Press a button whenever you are ready to start the real experiment, {}!' if not dutch else\
'Druk op een knop wanneer je klaar bent om het echte experiment te starten, {}!'

resp_to_continue = 'Respond correctly to these targets to continue!' if not dutch else\
                   'Reageer correct op deze target stimuli om door te gaan!'

test1 = 'Press {} and respond correctly to these targets to continue!' if not dutch else\
'Druk op {} en reageer correct op deze target stimuli om door te gaan!'

late_answer_text = 'Try to respond faster!' if not dutch else 'Probeer om sneller te reageren!'

neg_feedback_text = 'Wrong answer! Up for gap in the top, down for gap in the bottom!' if not dutch else 'Verkeerd antwoord!\
 Gebruik de bovenste toets als de opening aan de bovenkant is, en de onderste toets als de opening aan de onderkant is.'

pos_feedback_1 = 'Right! But you can be faster than this!' if not dutch else 'Correct! Maar je kunt sneller zijn dan dit!'
pos_feedback_2 = 'Right! But you won\'t have all this time in the real experiment!' if not dutch else 'Correct! Maar je zal niet zoveel tijd hebben in het echte experiment!'
pos_feedback_3 = 'Right! Pretty quick..can you go faster?' if not dutch else 'Correct! Redelijk snel...kun je nog sneller reageren?'
pos_feedback_4 = 'Right! Nice reaction time..try to lower it even further!' if not dutch else 'Correct! Goede reactietijd...probeer nog sneller te reageren!'
pos_feedback_5 = 'Right! Very fast!' if not dutch else 'Correct! Heel snel!'
pos_feedback_6 = 'Right! Impressively fast!!!' if not dutch else 'Correct! Indrukwekkend snel!!'

bye_text = 'Thanks for participating and goodbye!' if not dutch else 'Bedankt voor uw deelname en tot ziens.'

message_dict.update(wrong_key_text=wrong_key_text,
                    recap_message=recap_message,
                    end_practice=end_practice,
                    buttoN=buttoN,
                    space=space,
                    message_1_welcome=message_1_welcome,
                    message_2_target=message_2_target,
                    message_5_questions=message_5_questions,
                    message_6=message_6,
                    message_final=message_final,
                    resp_to_continue=resp_to_continue,
                    test1=test1,
                    late_answer_text=late_answer_text,
                    neg_feedback_text=neg_feedback_text,
                    pos_feedback_1=pos_feedback_1,
                    pos_feedback_2=pos_feedback_2,
                    pos_feedback_3=pos_feedback_3,
                    pos_feedback_4=pos_feedback_4,
                    pos_feedback_5=pos_feedback_5,
                    pos_feedback_6=pos_feedback_6,
                    bye_text=bye_text)

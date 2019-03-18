
################################################
################# Imports ######################
################################################
from psychopy import core, visual, logging, gui, event, prefs, data, sound, monitors
prefs.general['audioLib'] = ['pyo']
prefs.general['audioDriver'] = ['ASIO']
from numpy.random import random, randint, normal, shuffle
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import os
import sys
import numpy as np
from constants import *
from customFunctions import trialCreator

GlobalClock = core.Clock()  # Track time since experiment starts

#port = parallel.ParallelPort(address=0xd050) ################################
#port.setData(0)

################################################
############### Basic checks ###################
################################################

# check relative paths correct
_thisDir = os.path.abspath(os.path.dirname(__file__))
os.chdir(_thisDir)

################################################
####### Collect experiment session info ########
################################################

# Exp name
expName = 'Rhythm words'
# Define experiment info
expInfo = {'session':'001', 'participant':'001',
    'handedness':'', 'gender':'', 'native language': '', 'age': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName,)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()
# Create filename for data file (absolute path + name)
filename = _thisDir + os.sep + 'data/{0}'.format(expInfo['participant'])

################################################
################ Setup logfile #################
################################################

# save a log file for detailed verbose info
logFile = logging.LogFile(filename+'.log', level=logging.DATA)
# this outputs to the screen, not a file
logging.console.setLevel(logging.WARNING)

################################################
################# Variables ####################
################################################
# beats
binary_boi = sound.Sound(os.path.join('Stimuli', 'Tones', 'binary_beat.wav'))
ternary_boi = sound.Sound(os.path.join('Stimuli', 'Tones', 'ternary_beat.wav'))


# setup window
mon = monitors.Monitor(name = 'OptiPlex 7440',
                        width = 1920,
                        distance = 80)
mon.setWidth(80)
mon.setSizePix([1920, 1080])

win = visual.Window(fullscr=True,
                size = [1920, 1080],
                monitor=mon,
                units='deg',
                allowGUI=False)

trialClock = core.Clock()

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess 60Hz

with open('data/{}participant_info.txt'.format(expInfo['participant']), 'w') as log_file:
    log_file.write('Session\t' +
                    'Participant\t' +
                    'Handedness\t' +
                    'Gender\t' +
                    'Native_language\t' +
                    'Age\t' +
                    'frameRate\t' + '\n')
 
    log_file.write('\t'.join([str(expInfo['session']),
                            str(expInfo['participant']),
                            str(expInfo['handedness']),
                            str(expInfo['gender']),
                            str(expInfo['native language']),
                            str(expInfo['age']),
                            str(expInfo['frameRate'])]) + '\n')
log_file.close()

################################################
########## Trial list construction #############
################################################

# Main sentences
main_conditions = [sub_cong, sub_incong1, obj_cong, obj_incong1, obj_incong2,sub_neut, obj_neut]  
main_probes = [probe_mc_pos, probe_mc_neg, probe_rc_subpos_objneg, probe_rc_subneg_objpos,]
sentence_list = trialCreator(main_conditions, main_probes) # using function in customFunctions.py script to randomise and assemble sentences and probes

# Combining main and assorted trials into one list
all_trials = sentence_list
all_trials = data.TrialHandler(trialList = all_trials[:], nReps = 1, method = 'random', extraInfo = expInfo, name = 'all_trials')
thisTrial = all_trials.trialList[0]  # so we can initialise stimuli with some values

# Practice trials
prac_list = [ {**prac[i], **prac_probes[i]} for i in range(len(prac)) ]
prac_list = data.TrialHandler(trialList = prac_list[:], nReps = 1, method = 'sequential', extraInfo = expInfo, name = 'practice_trials')
thisPracTrial = prac_list.trialList[0]  # so we can initialise stimuli with some values

################################################
############## Run experiment ##################
################################################

try: 
    # ==== SETUP TRIAL OBJECTS ==== #
    message1 = visual.TextStim(win, pos=[0,+6], color=FGC, height=.7, alignHoriz='center', name='topMsg', text="placeholder") 
    message2 = visual.TextStim(win, pos=[0,-3], color=FGC, alignHoriz='center', name='bottomMsg', text="placeholder") 
    fixation = visual.TextStim(win,  pos=[0,0], color=FGC, alignHoriz='center', text="+")
    fixation2 = visual.TextStim(win,  pos=[0,0], color='black', height=1.05, alignHoriz='center', text="+")
    endMessage = visual.TextStim(win,  pos=[0,0], color=FGC, alignHoriz='center', text="The end! Thank you for participating :)")
    space_cont = visual.TextStim(win, pos=[0,0], color=FGC, text="Press space to continue")
    too_slow = visual.TextStim(win, pos=[0,0], color=FGC, text="Too slow: respond quicker next time")
    feedback = visual.TextStim(win, pos=[0,0], color=FGC, text="placeholder")
    introText = visual.TextStim(win, pos=[0,0], color=FGC, text="Placeholder")
    probe_text = visual.TextStim(win, pos=[0,0], color=FGC, alignHoriz='center', name='top_probe', text="placeholder")
    GSI = visual.RatingScale(win, name='GSI', marker='triangle',
                             textSize = 0.4, showValue = False, acceptText = 'confirm',
                              size=1.5, pos=[0.0, -0.4], 
                              choices=['Completely\n Disagree', 'Strongly\n Disagree',
                                         'Disagree', 'Neither Agree\n or Disagree', 'Agree',
                                          'Strongly\n Agree', 'Completely\n Agree'],
                             tickHeight=-1)
    response_keys = visual.TextStim(win, pos=[0,-5], height = .5, color=FGC, text="respond:'y' 'n' or 'd'")
    response_keys_check = visual.TextStim(win, pos=[0,-5], height = .5, color=FGC, text="respond:'1', '2', or '3'")

    break_text = visual.TextStim(win, pos=[0,0], color=FGC, text="Take a break and stretch for 15 seconds!")

    inst_image = visual.ImageStim(win, pos = [0,+1],)
    beat_indicator = visual.ImageStim(win, pos = [0,0])
    no_meter = visual.TextStim(win,  pos=[0,0], color=FGC, alignHoriz='center', text="(no meter)")

    # ==== OTHER TRIAL VARIABLES ==== #
    clock = core.Clock()

    # ===== LOG FILES ====== #
    # File for all trial information 
    with open('data/{}trial_log.txt'.format(expInfo['participant']), 'w') as log_file:
        log_file.write('Trial\t' + 
                        'Beat\t' + 
                        'Sentence\t' + 
                        'Sentence_extraction\t' + 
                        'Congruency\t' + 
                        'Probe\t' + 
                        'Probe_clause\t' + 
                        'Response\t' + 
                        'Accuracy\t' + 
                        'RT\t' + '\n')
    log_file.close()

    ################################################
    ############## START EXPERIMENT ################
    ################################################
    
    win.mouseVisible = False
    
    # ===== PRACTISE TRIALS INTRO ====== #
    counter = 0
    while counter < len(part1Intro):
        # === set top text === #
        message1.setText(part1Intro[counter]) 
        # === set bottom text === #
        if counter == 0:
            message2.setText(bottom_text[0])
        elif counter in range(1, (len(part1Intro) - 1)):
            message2.setText(bottom_text[1])
            if counter == 1:
                thisKey = event.waitKeys()
                if thisKey[0] in ['b']:
                    binary_boi.play()
                elif thisKey[0] in ['t']:
                    ternary_boi.play()
            if counter == 2:
                inst_image.setImage(os.path.join('Stimuli', 'Instructions', 'sub_incong.png'))
                inst_image.size = [10,4]
                inst_image.draw()
            if counter == 4:
                inst_image.setImage(os.path.join('Stimuli', 'Instructions', 'sub_congs.png'))
                inst_image.size = [25,15]
                inst_image.pos = [0,-4]
                inst_image.draw()
            if counter == 5:
                inst_image.setImage(os.path.join('Stimuli', 'Instructions', 'obj_congs.png'))
                inst_image.size = [25,15]
                inst_image.pos = [0,-4]
                inst_image.draw()
        else: 
            message2.setText(bottom_text[2])
        # === display instructions and wait === #
        message1.draw()
        message2.draw() 
        win.logOnFlip(level=logging.EXP, msg='Display Instructions%d'%(counter+1))
        win.flip()
        # === check for a keypress === #
        thisKey = event.waitKeys()
        if thisKey[0] in ['q','escape']:
            core.quit()
        elif thisKey[0] == 'backspace' and counter > 0:
            counter -= 1
        elif thisKey[0] == 'space':
            counter += 1

    # ===== PRACTICE TRIALS ====== #
    trial_num = 0
    for thisPracTrial in prac_list:  
        trial_num += 1
        # Abbeviate parameter names... e.g. thisPracTrial['beat_type'] becomes beat_type
        if thisPracTrial != None:
            for paramName in thisPracTrial:
                exec('{} = thisPracTrial[paramName]'.format(paramName))

        probe_resp = event.BuilderKeyResponse()
        
        ####====SETUP TRIAL COMPONENTS LIST====####
        # initialize trial components list
        trialComponents = []
        audio_stim = sound.Sound( str(os.path.join('Stimuli', 'Audio', 'Practise', ('sent' + str(sent_number + 1) + '.wav'))) ) 
        trialComponents.extend([audio_stim,]) # add audio stim to trialComponents list

        # set probe text for the trial
        probe_text.setText(probe)

        ####====BASIC ROUTINE CHECKS====####
        continueRoutine = True
        # keep track of which components have finished

        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        t = 0
        trialClock.reset()  # clock
        frameN = -1

        ####====START PRACTISE TRIAL ROUTINE====####
        while continueRoutine: 
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            
            ##### 1. start/stop beat_stim  #####
            if t >= 0.0 and audio_stim.status == NOT_STARTED:
                # keep track of start time/frame for later
                audio_stim.tStart = t
                audio_stim.frameNStart = frameN  # exact frame index
                audio_stim.play()  # start the sound (it finishes automatically)
                fixation.setAutoDraw(True)

            ##### 3.  check if all components have finished #####
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished 
            
            ##### 4.  refresh the screen #####
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        ####====Ending Trial Routine====####
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        audio_stim.stop()  # ensure sound has stopped at end of routine
        fixation.setAutoDraw(False)

        core.wait(probe_delay)

        ####====Probe====####
        # 3.  display probe text e.g. "The boy helped the girl?" #####
        probe_text.tStart = t
        probe_text.setAutoDraw(True)
        response_keys.setAutoDraw(True)

        ####====check for response====##### 
        probe_resp.tStart = t
        win.callOnFlip(probe_resp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
        thing = True
        while thing: 
            win.flip()
            theseKeys = event.getKeys(keyList=['y', 'n', 'd'])
            if len(theseKeys) > 0:  # at least one key was pressed
                probe_text.setAutoDraw(False)
                response_keys.setAutoDraw(False)
                probe_resp.keys = theseKeys[-1]  # just the last key pressed
                probe_resp.rt = probe_resp.clock.getTime()
                # was this 'correct'?
                if probe_resp.keys == 'n' and (trial_num == 1 or trial_num == 2 or trial_num == 6):
                    probe_resp.corr = 1
                    feedback.setText("correct")
                    feedback.draw()
                    thing = False
                elif probe_resp.keys == 'y' and (trial_num == 3 or trial_num == 4 or trial_num == 5):
                    probe_resp.corr = 1
                    feedback.setText("correct")
                    feedback.draw()
                    thing = False
                elif probe_resp.keys == 'd':
                    probe_resp.corr = 0
                    feedback.setText("(don't know)")
                    feedback.draw()
                    thing = False
                else:
                    probe_resp.corr = 0
                    feedback.setText("incorrect")
                    feedback.draw()
                    thing = False
        win.flip()
        core.wait(1)

        ####====Check if response is too slow====####
        if probe_resp.rt > probe_duration:
            too_slow.draw()
            win.flip()
            core.wait(1) 
        
        ####====Space to continue====####
        event.clearEvents(eventType='keyboard')
        space_cont.draw()
        win.flip()
        thisKey = event.waitKeys(keyList=['space'])
        while not 'space' in thisKey:
            thisKey = event.waitKeys(keyList=['space'])
        core.wait(1)
    
    # ===== INSTRUCTIONS 2 ====== #
    counter = 0
    while counter < len(part2Intro):
        message1.setText(part2Intro[counter])
        if counter == 0:
            message2.setText(bottom_text[0])
        elif counter in range(1, (len(part2Intro) - 1)):
            message2.setText(bottom_text[1])
        else: 
            message2.setText(bottom_text[2])
        #display instructions and wait
        message1.draw()
        message2.draw() 
        win.logOnFlip(level=logging.EXP, msg='Display Instructions%d'%(counter+1))
        win.flip()
        #check for a keypress
        thisKey = event.waitKeys()
        if thisKey[0] in ['q','escape']:
            core.quit()
        elif thisKey[0] == 'backspace' and counter > 0:
            counter -= 1
        else:
            counter += 1
    
    trial_num = 0 # initialise trial number

    #port.setData('G0') # start of trials marker
    #core.wait(.001)
    #port.setData(0)

    # ===== MAIN TRIALS ====== #
    for thisTrial in all_trials:  

        trial_num += 1
        ####====ABBREVIATE PARAMETER NAMES====####
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))

        # Check for break trial
        if trial_num % break_frequency == 0:
            break_text.draw()
            win.flip()
            core.wait(break_duration)

        probe_resp = event.BuilderKeyResponse() # initialising
        check_resp = event.BuilderKeyResponse() # initialising

        # create counter for adding the manipulation check bit every 4/5 trials
        if trial_type == 'catch':
            check_trial = True
        else:
            check_trial = False
            check_resp.corr = 'NA'
            check_resp.keys = 'NA'
        
        ####====SETUP TRIAL COMPONENTS LIST====####
        # initialize trial components list
        trialComponents = []

        # add auditory stimuli component
        audio_stim = sound.Sound( str(os.path.join('Stimuli', 'Audio', (extraction + '_' + congruency), ('sent' + str(sent_number + 1) + '.wav'))) ) 

        if beat_type == 'binary':
            meter_ITI = 2 * beat_freq
        elif beat_type == 'ternary':
            meter_ITI = 3 * beat_freq

        trialComponents.extend([audio_stim],) # add beat stim to trialComponents list
        # set probe text for the trial
        probe_text.setText(probe)

        ####====BASIC ROUTINE CHECKS====####
        continueRoutine = True
        # keep track of which components have finished
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        if congruency != 'neutral':
            beat_indicator_path = os.path.join('Stimuli', 'Instructions', 'beat_ind', beat_type + '_' + congruency + '.png')
            beat_indicator.setImage(beat_indicator_path)
            beat_indicator.draw()
        else:
            no_meter.draw()
        win.flip()
        core.wait(1)

        t = 0
        frameN = -1
        sent_marker = True
        trialClock.reset()  # clock

        ####====START MAIN TRIAL ROUTINE====####
        while continueRoutine: 
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            ##### 1. start/stop beat_stim  #####
            if t >= 0.0 and audio_stim.status == NOT_STARTED:
                # keep track of start time/frame for later
                #port.setData(trial_ref) # start of tones marker + trial ref
                #core.wait(.0001)
                #port.setData(0)
                audio_stim.tStart = t
                audio_stim.frameNStart = frameN  # exact frame index
                audio_stim.play()  # start the sound (it finishes automatically)
                fixation.setAutoDraw(True)
            
            if beat_type != 'nonaccent':
                if 0 <= (t - (audio_stim.tStart + sound_delay)) % meter_ITI <= .1:
                    fixation2.draw() # i.e. this will be shown for 1 screen refresh (~.066 seconds)


            # EEG marker for sentence start
            if (t - (audio_stim.tStart + sound_delay)) >= sent_offset*beat_freq and sent_marker:
                #port.setData('G1') # start of tones marker + trial ref
                #core.wait(.0001)
                #port.setData(0)
                #print(t)
                #test_text.setAutoDraw(True)
                sent_marker = False

            ##### 2.  check if all components have finished #####
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            ##### 3.  refresh the screen #####
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
            
        ####====Ending Trial Routine====####
        audio_stim.stop()  # ensure sound has stopped at end of routine
        #port.setData('G2') # start of tones marker
        #core.wait(.001)
        #port.setData(0)
        fixation.setAutoDraw(False)
        #test_text.setAutoDraw(False)

        core.wait(probe_delay)

        ####====Probe====####
        # 3.  display probe text e.g. "The boy helped the girl?" #####
        probe_text.tStart = t
        probe_text.setAutoDraw(True)
        response_keys.setAutoDraw(True)

        ####====check for response====##### 
        probe_resp.tStart = t
        win.callOnFlip(probe_resp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
        thing = True
        #port.setData(probe_ref) # start of trials marker
        #core.wait(.001)
        #port.setData(0)
        while thing: 
            win.flip()
            theseKeys = event.getKeys(keyList=['y', 'n', 'd'])
            if len(theseKeys) > 0:  # at least one key was pressed
                probe_text.setAutoDraw(False)
                response_keys.setAutoDraw(False)
                probe_resp.keys = theseKeys[-1]  # just the last key pressed
                probe_resp.rt = probe_resp.clock.getTime()
                # was this 'correct'?
                if probe_resp.keys == 'y' and pos_neg == 'positive':
                    probe_resp.corr = 1
                    feedback.setText("correct")
                    feedback.draw()
                    # EEG marker
                    #port.setData('R11') # start of trials marker
                    #core.wait(.001)
                    #port.setData(0)
                elif probe_resp.keys == 'n' and pos_neg == 'negative':
                    probe_resp.corr = 1
                    feedback.setText("correct")
                    feedback.draw()
                    # EEG marker
                    #port.setData('R21') # start of trials marker
                    #core.wait(.001)
                    #port.setData(0)
                elif probe_resp.keys == 'n' and pos_neg == 'positive':
                    probe_resp.corr = 0
                    feedback.setText("incorrect")
                    feedback.draw()
                    # EEG marker
                    #port.setData('R22') # start of trials marker
                    #core.wait(.001)
                    #port.setData(0)
                elif probe_resp.keys == 'y' and pos_neg == 'negative':
                    probe_resp.corr = 0
                    feedback.setText("incorrect")
                    feedback.draw()
                    # EEG marker
                    #port.setData('R12') # start of trials marker
                    #core.wait(.001)
                    #port.setData(0)
                elif probe_resp.keys == 'd':
                    probe_resp.corr = 0
                    feedback.setText("(don't know)")
                    feedback.draw()
                    # EEG marker
                    #port.setData('R32') # start of trials marker
                    #core.wait(.001)
                    #port.setData(0)
                thing = False
        win.flip()
        core.wait(.5)

        ####====Check if response is too slow====####
        if probe_resp.rt > probe_duration:
            too_slow.draw()
            win.flip()
            core.wait(2) 

        with open('data/{}trial_log.txt'.format(expInfo['participant']), 'a') as log_file: 
            log_file.write('\t'.join([str(trial_num),
                str(beat_type),
                str(sent_stim),
                str(extraction),
                str(congruency),
                str(probe),
                str(clause),
                str(probe_resp.keys),
                str(probe_resp.corr),
                str(probe_resp.rt)]) + '\n')
            log_file.close()
        core.wait(.8)
        
        ####====Space to continue====####
        event.clearEvents(eventType='keyboard')
        space_cont.draw()
        win.flip()
        thisKey = event.waitKeys(keyList=['space'])
        while not 'space' in thisKey:
            thisKey = event.waitKeys(keyList=['space'])

        core.wait(.5)
    logging.flush()

    #port.setData('G3') # start of trials marker
    #core.wait(.001)
    #port.setData(0)
    
    ################################################
    ############## GSI QUESTIONNAIRE ################
    ################################################
    
    # ===== INSTRUCTIONS 3 ====== #
    counter = 0
    while counter < len(part4Intro):
        message1.setText(part4Intro[counter])
        if counter == 0:
            message2.setText(bottom_text[0])
        elif counter in range(1, (len(part4Intro) - 1)):
            message2.setText(bottom_text[1])
        else: 
            message2.setText(bottom_text[2])
        #display instructions and wait
        message1.draw()
        message2.draw() 
        win.logOnFlip(level=logging.EXP, msg='Display Instructions%d'%(counter+1))
        win.flip()
        #check for a keypress
        thisKey = event.waitKeys()
        if thisKey[0] in ['q','escape']:
            core.quit()
        elif thisKey[0] == 'backspace':
            counter -= 1
        else:
            counter += 1

    with open('data/{}questionnaire_log.txt'.format(expInfo['participant']), 'w') as log_file:
        log_file.write('Question_num\t' +
                       'Question\t' +
                       'Response' + '\n')

        win.mouseVisible = True
        quest_num = 1 # initialising counter 
        for question in gsi_part1:
            message1.setText(question)
            while GSI.noResponse: 
                message1.draw()
                GSI.draw()
                win.flip()
            response = GSI.getRating()
            #======WRITE DATA TO FILE======#    
            log_file.write('\t'.join([str(quest_num),
                            str( question.replace('\n','') ),
                            str( response.replace('\n','') )]) + '\n')
            
            log_file.flush()
            GSI.noResponse = True
            GSI.response = None
            quest_num += 1
            core.wait(.2)
        
        quest_num = 1 # initialising counter 
        for question in gsi_part2:
            message1.setText(question)
            GSI = visual.RatingScale(win, name='GSI', marker='triangle',
                             textSize = 0.4, showValue = False, acceptText = 'confirm',
                              size=1.5, pos=[0.0, -0.4], 
                              choices= gsi_part2_scales[quest_num - 1],
                             tickHeight=-1)
            while GSI.noResponse: 
                message1.draw()
                GSI.draw()
                win.flip()
            response = GSI.getRating()
            #======WRITE DATA TO FILE======#    
            log_file.write('\t'.join([str((quest_num + 31)),
                            str( question.replace('\n','') ),
                            str( response.replace('\n','') )]) + '\n')
            
            log_file.flush()
            GSI.noResponse = True
            GSI.response = None
            quest_num += 1
            core.wait(.2)
    endMessage.draw()
    win.flip()
    core.wait(5)  
finally:
    win.close()
    core.quit()

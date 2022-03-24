import psychopy
from psychopy import core, visual, event
from psychopy.visual import ShapeStim
import socket
import json
import glob
import numpy as np
import os.path as op
import scipy.stats
import sys, getopt
import time
import pickle
import datastruct 
import pandas as pd
import seaborn as sns
from textwrap import dedent

        
def check_abort(keys):
    if 'escape' in keys:
        core.quit()
        
#annoying function because setting opacity for textstim doesn't work    
def draw_error(win, nframes, fixation_color):
    for frameN in range(int(nframes)):    
        error = visual.TextStim(win,
                color = fixation_color,
                text='+',
                opacity = float((frameN % 8) >= 4))
        error.draw()
        win.flip()
        check_abort(event.getKeys())
    
def main(arglist):

    ##################################
    #### Parameter Initialization ####
    ##################################
    
    # Get the experiment parameters
    mode = arglist.pop(0)
    p = datastruct.Params(mode)
    p.set_by_cmdline(arglist)
    p.set_rand_state()
    if p.run_mode == 'practice':
        p.load_practice_info(op.abspath('./stimuli/output_triplets_practice_rand_vals.csv'))
    else:
        p.load_exp_info(op.abspath('./stimuli/output_triplets_tidy_fmri.csv'))
    p.run_times_to_itis()
    
    ##################################
    #### Window Initialization ####
    ##################################

    # Create a window
    win = p.launch_window(p)

    #hide mouse
    event.Mouse(visible = False)
    win.mouseVisible = False
    
    ########################
    #### Visual Objects ####
    ########################

    #fixation cross
    fixation = visual.TextStim(win,
        color = p.text_color,
        text='+')

    #Semantic labels
    semantic1 = visual.TextStim(win,
        color = p.text_color,
        pos=(-p.im_size*2/3, -p.im_size*2/3),
        text='Living')

    semantic2 = visual.TextStim(win,
        color = p.text_color,
        pos=(p.im_size *2/3, -p.im_size*2/3),
        text='Not Living')

    
    #chosen text boxe
    rightbox = visual.Rect(win,
                            pos=(p.im_size*2/3, 0),
                            size=p.im_size*1.1,
                            lineWidth=0,
                            fillColor=p.chosen_rect_color)
    leftbox = visual.Rect(win,
                            pos=(-p.im_size*2/3, 0),
                            size=p.im_size*1.1,
                            lineWidth=0,
                            fillColor=p.chosen_rect_color)

    #feedback text
    feedback_cues = dict()
    feedback_cues['pos'] = visual.TextStim(win,
        color = p.rew_color,
        text='+')
        
    feedback_cues['neg'] = visual.TextStim(win,
        color = '#af392a',
        text='+')

    feedback_cues['missed'] = visual.TextStim(win,
        color = '#af392a',
        text='Too slow')

    #loading text
    load = visual.TextStim(win,
        color = p.text_color,
        text='Loading stimuli. Please wait...')
    load.draw()
    win.flip()

    root_cue = []
    left_cue = []
    right_cue = []
    for n in range(p.ntrials):
        root_cue.append(visual.ImageStim(
                        win=win,
                        name='root' + str(n),
                        image=op.join(p.im_path, p.run_info['root'][n]),
                        pos=(0, 0),
                        size=(p.im_size,p.im_size)))

        left_cue.append(visual.ImageStim(
                        win=win,
                        name='left_cue' + str(n),
                        image=op.join(p.im_path, p.run_info['LeftIm'][n]),
                        pos=(-p.im_size*2/3, 0),
                        size=(p.im_size,p.im_size)))

        right_cue.append(visual.ImageStim(
                        win=win,
                        name='right_cue' + str(n),
                        image=op.join(p.im_path, p.run_info['RightIm'][n]),
                        pos=(p.im_size*2/3, 0),
                        size=(p.im_size,p.im_size)))

    ########################
    #### Instructions ####
    ########################
    if p.run_mode == 'practice':
        for n,txt in enumerate(p.instruct_text):
            message = visual.TextStim(win,
                color = p.text_color,
                text=dedent(txt))
            message.draw()
            win.flip()
            keys = event.waitKeys(keyList  = ['1'])
        
            #show single image example
            if n==2:
                example = visual.ImageStim(
                                win=win,
                                name='root' + str(n),
                                image=op.join(p.instruct_stim_path,'root_inst.jpg'),
                                pos=(0, 0),
                                size=(p.im_size,p.im_size))
                example.draw()
                semantic1.draw()
                semantic2.draw()
                win.flip()
                keys = event.waitKeys(keyList  = ['1','2'])
            #show decision example
            if n==4:
                left_example = visual.ImageStim(
                                win=win,
                                name='left_cue' + str(n),
                                image=op.join(p.instruct_stim_path, 'im1_inst.jpg'),
                                pos=(-p.im_size*2/3, 0),
                                size=(p.im_size,p.im_size))

                right_example = visual.ImageStim(
                                win=win,
                                name='right_cue' + str(n),
                                image=op.join(p.instruct_stim_path, 'im2_inst.jpg'),
                                pos=(p.im_size*2/3, 0),
                                size=(p.im_size,p.im_size))
                left_example.draw()
                right_example.draw()
                fixation.draw()
                win.flip()
                keys = event.waitKeys(keyList  = ['1','2'])
    else:
        for n,txt in enumerate(p.instruct_text):
            txt = txt.replace('RUN',str(p.run))
            txt = txt.replace('TOTAL',str(p.nruns))
            
            if int(p.run) <= int(p.nruns)/2:
                alg = 'ONE'
            else:
                alg = 'TWO'
            txt = txt.replace('ALG',alg)              
                
            message = visual.TextStim(win,
                color = p.text_color,
                text=dedent(txt))
            message.draw()
            win.flip()
            wait = event.waitKeys(keyList  = ['1'])
            
            
        if int(p.run) == int(p.nruns)/2 + 1: #first run of switch
            for n,txt in enumerate(p.alg_change_notification):
                message = visual.TextStim(win,
                    color = p.text_color,
                    text=dedent(txt))
                message.draw()
                win.flip()
                wait = event.waitKeys(keyList  = ['2'])


    ########################
    #### Run Experiment ####
    ########################

    #start timer
    clock = core.Clock()
    
    #wait for experimenter to start experiment
    if p.run_mode == 'fmri':
        wait = visual.TextStim(win,
                    color = p.text_color,
                    text='Please wait for the experimenter to start the experiment')
        wait.draw()
        win.flip()
        keys = event.waitKeys(keyList  = ['space'], timeStamped = clock)
    
    #start timer
    check_abort(event.getKeys())
    fixation.draw()
    win.flip()
    clock = core.Clock()

    #scanner init
    core.wait(p.init_wait_time)

    p.semantic_resp = []
    p.semantic_rt = []
    p.choice = []
    p.choice_rt = []
    p.root_times = []
    p.choice_times = []
    p.feedback_times = []
    p.rewards = []
    p.correct = []
    p.too_late_keypresses = [] #log responses that are too slow
    p.bank = 0
        
    for n in range(p.ntrials):
        
        #root cue period
        root_cue[n].draw()
        semantic1.draw()
        semantic2.draw()
        win.flip()

        #wait for keys
        rt_clock = clock.getTime()
        p.root_times.append(rt_clock)
        keys = psychopy.event.waitKeys(maxWait = p.first_decision_dur,
            keyList = ['1','2'],
            timeStamped = clock)
        if keys is None:
            resp = np.NaN
            p.semantic_resp.append(resp)
            p.semantic_rt.append(np.NaN)
        else:
            resp = keys[0][0]
            p.semantic_resp.append(resp)
            p.semantic_rt.append(keys[0][1] - rt_clock)

        # wait out rest of choice period
        while clock.getTime() < rt_clock + p.first_decision_dur:
            None

        #check for missed responses
        nframes = p.feedback_dur * win.framerate
        if keys is None:
            draw_error(win, nframes, p.too_slow_color)
        
        #ISI period
        check_abort(event.getKeys())
        fixation.draw()
        win.flip()
        
        #prepare decision period stims
        fixation.draw()
        left_cue[n].draw()
        right_cue[n].draw()
        
        #wait ISI
        while clock.getTime() < p.root_times[-1] + p.first_decision_dur +  p.isi_root[n]:
            None

        #Decision Period
        win.flip()

        #wait for keys
        rt_clock = clock.getTime()
        p.choice_times.append(rt_clock)
        keys = psychopy.event.waitKeys(maxWait = p.second_decision_dur,
            keyList = ['1','2'],
            timeStamped = clock)
        
        #record keys if there are any
        if keys is not None:
            resp = keys[0][0]
            p.choice.append(resp)
            p.choice_rt.append(keys[0][1] - rt_clock)
        
        # wait out rest of choice period
        while clock.getTime() < rt_clock + p.second_decision_dur:
            None
        
        #Second ISI period        
        fixation.draw()
        win.flip()
        
        #check for late keypresses
        late_keys = psychopy.event.waitKeys(maxWait = p.late_wait_duration,
            keyList = ['1','2'],
            timeStamped = clock)
        if keys is None:
            if late_keys is not None:
                p.choice.append(late_keys[0][0])
                p.choice_rt.append(late_keys[0][1] - rt_clock)
            else:
                resp = np.NaN
                p.choice.append(resp)
                p.choice_rt.append(np.NaN)
                
        #check for abort cue
        check_abort(event.getKeys())

        #wait out ISI
        while clock.getTime() < p.choice_times[-1] + p.second_decision_dur + p.isi_choice[n]:
            None
        
        #check for missed responses
        if keys is None:
            p.feedback_times.append(clock.getTime())
            draw_error(win, nframes, p.too_slow_color)
            p.bank = p.bank - 1
            p.rewards.append(np.NaN)
        
        else:
            correct = False
            #check whether selected option was correct according to run algorithm
            if p.block_order_IT_V2[n] == 'IT':
                
                if resp == '1' and p.IT_most_similar_lr[n] == 'left':
                    correct = True
                elif resp == '2' and p.IT_most_similar_lr[n] == 'right':
                    correct = True
                    
            elif p.block_order_IT_V2[n] == 'V2':
                
                if resp == '1' and p.V2_most_similar_lr[n] == 'left':
                    correct = True
                elif resp == '2' and p.V2_most_similar_lr[n] == 'right':
                    correct = True
            
            p.correct.append(correct)    
            #draw reward according to correct/incorrect
            if correct: 
                rew = scipy.stats.bernoulli.rvs(p.rew_probs[n])
            else:
                rew = scipy.stats.bernoulli.rvs(1 - p.rew_probs[n])
            
            # print(resp, p.block_order_IT_V2[n], p.IT_most_similar_lr[n], p.V2_most_similar_lr[n], correct, rew, p.rew_probs[n])
            
            #display reward
            if rew:
                feedback_cues['pos'].draw()
                p.bank = p.bank + 1
            else: 
                feedback_cues['neg'].draw()            
                p.bank = p.bank - 0
                
            p.rewards.append(rew)
        
            #execute feedback period
            win.flip()
            p.feedback_times.append(clock.getTime())
            core.wait(p.feedback_dur)
             
        #iti period
        fixation.draw()
        win.flip()
        while clock.getTime() < p.feedback_times[-1] + p.feedback_dur + p.iti[n]:
            None

        check_abort(event.getKeys())


    #save data
    out_f = op.join(p.outdir,
                    '_'.join([p.sub,'run',str(p.run),p.run_mode]) + '.pkl')
    while op.exists(out_f):
        out_f = out_f[:-4] + '+.pkl'
        
    with open(out_f, 'wb') as output:
        pickle.dump(p, output, pickle.HIGHEST_PROTOCOL)
    
    #wait for HRF to die down
    if p.run_mode == 'fmri':
        core.wait(p.end_run_wait)
        print('finish time',clock.getTime())
        print(p.bank)
        check_abort(event.getKeys())
        
    #if in behavior mode, just keep calling this function until experiment ends
    if p.run_mode in ['behavior','fmri','experimenter'] and int(p.run) < p.nruns:
        
        argv = [p.run_mode, '-s', p.sub, '-r', str(int(p.run) + 1)]
        main(argv)    
    
    core.quit()
    
    
if __name__ == "__main__":
    
    main(sys.argv[1:])    
   
   

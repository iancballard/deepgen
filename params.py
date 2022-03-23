from copy import deepcopy
import os.path as op
from textwrap import dedent

#base parameters for all runs
base = dict(

    init_wait_time = 1,
    nruns = 12, #12 25 stim blocks = 300 total stimuli
    block_reward_probabilities = [.9,.9,.775,.775,.65,.65],
    experimenter_mode_timing = 1.75, #ISI/ITIs for running in testing mode
    first_decision_dur = 2,
    second_decision_dur = .75,
    feedback_dur = 1,
    late_wait_duration = 1, #record keypressed after second_decision_dur for this long (make sure shorter than shortest ISI)
    too_slow_color = '#992020',
    text_color = '#999999',
    chosen_rect_color = '#999999',
    window_color = '#0a0a0a',#'#545454',
    rew_color = '#2aaf39',
    im_size = 7,
    test_refresh = True,
    monitor_name = 'mbpro',
    monitor_units = 'deg',
    full_screen = True,
    im_path = op.abspath('./stimuli/images_resize/'),
    instruct_stim_path = op.abspath('./stimuli/example_stims/'),
    outdir = op.abspath('./data/'),

)

practice = deepcopy(base)

practice.update(
    run_mode = 'practice',
    im_path = op.abspath('./stimuli/practice_stims/'),
    instruct_text = ["""
                    Welcome to the experiment.
                    Today you will be making decisions about images.
                    The experiment will take about 90 minutes.
                    Press the "1" key to proceed through the instructions.
                    """,
                    """
                    Each trial of the experiment is composed of two parts.
                    In the first part of each trial, you will see an image and respond
                    based on whether the image is primarily of a living
                    or a nonliving thing. If there are both living and nonliving things
                    in the image, just use your best judgment. 
                    Make your responses with the "1" and "2" keys.
                    """,
                    """
                    You should pay close attention
                    to the image because it will be important for the second part
                    of the trial. 
                    You will have 2 seconds to respond.
                    Press "1" to see an example.
                    """,
                    """
                    In the second part of the trial you will see a pair of images.
                    Select the image that you think is more similar to the 
                    image from the first part of the trial
                    (in this case, the easel you just saw).
                    """,
                    """
                    Select the left with the "1" key and the right with the "2" key.
                    You will have .75 seconds to respond.
                    The fixation cross will flicker red if you respond too slowly.
                    If you respond too slowly, you will lose points.
                    In the following example, you should select the image
                    that seems more similar to the easel you just saw.
                    """,
                    """
                    A computer algorithm determines which of the two
                    images is the most similar. If you select the image that that the computer
                    thinks is more similar to the first image, you will have a higher probability
                    of winning a point.
                    It is possible to select the image that the computer thinks is most similar and
                    still not win a point, but overall the more that you select images that
                    agree with the computer, the more points you will earn.
                    """,
                    """
                    If you win a point, the fixation cross will turn green.
                    If you do not win a point, the fixation cross will turn red.
                    """,
                    """
                    You will perform 12 blocks of the task during the main experiment.
                    The computer algorithm that picks which image is more similar
                    will stay the same within a block, but it will change between blocks.
                    Therefore, it is important to try to learn what the computer is doing on
                    each block. 
                    """,
                    """
                    After the experiment, one of the 12 blocks will be selected to count for real
                    and the the points you earned in that block will be added up as a bonus, with each
                    point being worth 50 cents. 
                    Therefore, make good choices for the potential to earn up to 5 dollars bonus.
                    If you have questions. Please ask the experimenter now.
                    """,
                    """
                    Press "1" to start a practice session.
                    The rewards do not count in the practice session,
                    so just try your hardest.
                    """]
)

behavior = deepcopy(base)
behavior.update(
    
    run_mode = 'behavior',
    instruct_text = ["""
                    You are about to begin run RUN out of TOTAL
                    Press the first key to when you are ready to begin.
                    """]
)

fmri = deepcopy(base)
fmri.update(
    
    run_mode = 'fmri',
    init_wait_time = 12,
    end_run_wait = 10,
    instruct_text = ["""
                    You are about to begin run RUN out of TOTAL
                    Press the first key to when you are ready to begin.
                    """]    
)

experimenter = deepcopy(behavior)
experimenter.update(
    
    run_mode = 'experimenter',
  
)


from copy import deepcopy
import os.path as op
from textwrap import dedent

#base parameters for all runs
base = dict(

    init_wait_time = 1,
    nruns = 12, #12 25 stim blocks = 300 total stimuli
    rew_prob = 1.0,
    experimenter_mode_timing = 1.75, #ISI/ITIs for running in testing mode
    first_decision_dur = 2,
    second_decision_dur = 1,
    feedback_dur = 1,
    late_wait_duration = .95, #record keypressed after second_decision_dur for this long (make sure shorter than shortest ISI)
    too_slow_color = '#992020',
    text_color = '#999999',
    chosen_rect_color = '#999999',
    window_color = '#0a0a0a',#'#545454',
    rew_color = '#2aaf39',
    im_size = 7,
    test_refresh = False,
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
                    Throughout the experiment there will be a cross at the center
                    of the screen. There will be images that appear on either side
                    of the cross. Look at the images while keeping your eyes focused
                    on the central cross. Try not to let your eyes move around when
                    you are looking at the images.
                    """,
                    """
                    Each trial of the experiment is composed of two parts.
                    In the first part of each trial, you will see an image.
                    This image may appear on the left or right side of the screen.
                    Look at the image while keeping your eyes focused on the
                    cross at the center of the screen. 
                    """,
                    """
                    You should pay close attention
                    to the image because it will be important for the second part
                    of the trial. 
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
                    You will have 1 second to respond.
                    The fixation cross will flicker red if you respond too slowly.
                    If you respond too slowly, you will lose points.
                    In the following example, you should select the image
                    that seems more similar to the easel you just saw.
                    """,
                    """
                    A computer algorithm determines which of the two
                    images is the most similar. If you select the image that that the algorithm
                    thinks is MORE similar to the first image, the fixation cross will turn green,
                    which tells you that you won a point.
                    """,
                    """
                    f you select the image that that the algorithm
                    thinks is LESS similar to the first image, the fixation cross will turn red,
                    which tells you that you lost a point.
                    """,
                    """
                    If you respond too slowly (after the images have disappeared),
                    the fixation cross will flicker red, and you will lose a point.
                    """,
                    """
                    You will perform 12 blocks of the task during the main experiment.
                    The computer algorithm that picks which image is more similar
                    will stay the same for the first 6 blocks. Therefore, you can carry
                    over what you have learned from block to block to keep improving your
                    earnings. After 6 blocks, the algorithm will change and you will have 
                    6 more blocks to learn how to respond with new algorithm. 
                    """,
                    """
                    It is important to try to learn what the algorithm is doing in order to 
                    earn the biggest bonus.
                    """,
                    """
                    As a tip, the left/right location of the images, on the both the first
                    and second part of each trial, is **NOT** part of either algorithm. You can 
                    safely ignore whether the image is on the left or right part of the screen 
                    throughout the entire experiment.
                    """,
                    """
                    After the experiment, one of the 12 blocks will be selected to count for real
                    and the the points you earned in that block will be added up as a bonus, with each
                    point being worth 50 cents. 
                    Therefore, make good choices for the potential to earn up to 10 dollars bonus.
                    Remember that responses that are too slow deduct from your point total.
                    """,
                    """
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
                    This is a Computer Aglorithm ALG block.
                    Press the first key to when you are ready to begin.
                    """],
    alg_change_notification = ["""
                    The algorithm selecting which of the images is most
                    similar has changed! This is the first block with the 
                    new algorithm. The new algorithm will decide whether you
                    get rewards for the rest of the experiment.
                    Press the SECOND key to continue.
                    """]
)

fmri = deepcopy(behavior)
fmri.update(
    
    run_mode = 'behavior',
    init_wait_time = 12,
    end_run_wait = 10,

    
)

experimenter = deepcopy(behavior)
experimenter.update(
    
    run_mode = 'experimenter',
  
)


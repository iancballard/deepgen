import sys, getopt
import time
import numpy as np
import pandas as pd
import os.path as op
import math
from psychopy.monitors import Monitor
from psychopy import core, visual, event, logging
from numpy.random import RandomState
pd.options.mode.chained_assignment = None  # suppress chained assignment warning

class Params(object):
    
    def __init__(self, mode, p_file='params'):
        """Initializer for the params object.
        Parameters
        ----------
        exp_name: string, name of the dict we want from the param file
        p_file: string, the name of a parameter file
        """
        

        self.mode = mode
        
        #read paramaters from file
        im = __import__(p_file)
        param_dict = getattr(im, mode)
        for key, val in param_dict.items():
            setattr(self, key, val)
        
        timestamp = time.localtime()
        self.timestamp = time.asctime(timestamp)
        self.date = time.strftime("%Y-%m-%d", timestamp)
        self.time = time.strftime("%H-%M-%S", timestamp)
        
    def set_by_cmdline(self,argv):
        #parse inputs
        help_str = 'feedback.py -s <subject_id> -r <run> -c <counterbalance>'
        try:
          opts, args = getopt.getopt(argv,"s:r:c:d",["subject=", "run=", "cb="])
          if len(opts) == 0:
              print(help_str)
              sys.exit(2)          
        except getopt.GetoptError:
          print(help_str)
          sys.exit(2)
      
        for opt, arg in opts:
          if opt == '-h':
             print(help_str)
             sys.exit()
          elif opt in ("-s", "--subject"):
             self.sub = arg
          elif opt in ("-r", "--run"):
             self.run = arg
          elif opt in ("-c", "--cb"):
             self.cb = arg
    
    def set_rand_state(self):
        self.hash_sub_id = sum(map(ord, self.sub))
        
    def load_exp_info(self, filename):
        rs = RandomState(self.hash_sub_id) #set random state
        df = pd.read_csv(filename)
            
        #shuffle the pandas dataframe 
        good_randomization = False
        while not good_randomization: #keep shuffling until blocks have reasonably balanced numbers of IT/V2 agreements/disagreements
        
            df = df.iloc[rs.permutation(len(df))]

            num_trial_per_block = df.shape[0] / self.nruns


            #shuffle Image1 and Image2 location
            left_right = []
            left_right_root = []
            block_id = []
            for i in range(self.nruns):
                lr = ['left']*int(num_trial_per_block/2) + ['right']*int(num_trial_per_block/2)
                lr_root = ['left']*int(num_trial_per_block/2) + ['right']*int(num_trial_per_block/2)
                
                if len(lr) < num_trial_per_block: #append one if ntrials ends up being odd
                    lr.append(rs.choice(['left','right']))
                    lr_root.append(rs.choice(['left','right']))
                rs.shuffle(lr)
                rs.shuffle(lr_root)
    
                left_right.extend(lr.copy())
                left_right_root.extend(lr_root.copy())
                block_id.extend(np.array([int(i) + 1]*int(num_trial_per_block)))

            df['left_right'] = left_right
            df['left_right_root'] = left_right_root
            df['run'] = block_id
        
            #figure out lr mappings and V1/V2 similarities
            left_stim = []
            right_stim = []
            IT_most_similar_lr = []
            V2_most_similar_lr = []

            for lr, im1, im2, it, v2 in zip(left_right, df['Image1'],df['Image2'],df['IT_most_similar'],df['V2_most_similar']):
    
                if lr == 'left':
                    left_stim.append(im1)
                    right_stim.append(im2)
        
                    similar_map = {'im1':'left','im2':'right'}
                else:
                    left_stim.append(im2)
                    right_stim.append(im1)
        
                    similar_map = {'im1':'right','im2':'left'}
    
                IT_most_similar_lr.append(similar_map[it])
                V2_most_similar_lr.append(similar_map[v2])   

            df['LeftIm'] = left_stim
            df['RightIm'] = right_stim
            df['IT_most_similar_lr'] = IT_most_similar_lr
            df['V2_most_similar_lr'] = V2_most_similar_lr

            #check to make sure no block has more than 14 trials where V2 and IT either both agree or both disagree 
            #This ensures that there is not too much correlation between V2 and IT within block
            bad_shuffle = False
            for run in range(1,13):
                run_info = df.set_index('run').loc[int(run)].reset_index()
            
                num_similar = sum(run_info['IT_most_similar_lr'] == run_info['V2_most_similar_lr'])
                if num_similar < 11 or num_similar > 14:
                    bad_shuffle = True
        
            if not bad_shuffle:
                good_randomization = True
                
        #set reward probabilities
        df['rew_probs'] = self.rew_prob

        #set block order of whether IT or V2 are rewarded
        possible_block_orders = [['IT']*int(self.nruns/2) + ['V2']*int(self.nruns/2),
                               ['V2']*int(self.nruns/2) + ['IT']*int(self.nruns/2)]
        block_order = possible_block_orders[rs.choice([0,1])]
        df['block_order'] = np.repeat(block_order, num_trial_per_block)

        self.ntrials = int(num_trial_per_block)
        self.exp_info = df
        

        #set run specific variables
        run_df = df.set_index('run').loc[int(self.run)].reset_index()
        self.run_info = run_df
        self.block_order_IT_V2 = run_df['block_order'].values
        self.left_right_root = run_df['left_right_root'].values
        self.rew_probs = run_df['rew_probs'].values 
        self.IT_most_similar_lr = run_df['IT_most_similar_lr'].values 
        self.V2_most_similar_lr = run_df['V2_most_similar_lr'].values 
        
    def load_practice_info(self, filename):
        df = pd.read_csv(filename)
        ntrials = df.shape[0]
        lr = ['left','right'] * int(ntrials/2)
        np.random.shuffle(lr)
        self.ntrials = df.shape[0]
        self.exp_info = df
        self.run_info = df
        self.block_order_IT_V2 = df['block_order'].values
        self.rew_probs = df['rew_probs'].values
        self.IT_most_similar_lr = df['IT_most_similar_lr'].values 
        self.left_right_root = lr
        self.V2_most_similar_lr = df['V2_most_similar_lr'].values
        print(df['IT_most_similar_lr'].values)
        
    def launch_window(self, test_refresh=True, test_tol=.5):
        """Load window info"""
        #taken from Mwaskom cregg
        try:
            mod = __import__("monitors")
        except ImportError:
            sys.exit("Could not import monitors.py in this directory.")

        try:
            minfo = getattr(mod, self.monitor_name)
        except IndexError:
            sys.exit("Monitor not found in monitors.py")

        fullscreen = self.full_screen
        size = minfo["size"] if fullscreen else (800, 600)

        monitor = Monitor(name=minfo["name"],
                          width=minfo["width"],
                          distance=minfo["distance"])
        monitor.setSizePix(minfo["size"])
        
        info = dict(units=self.monitor_units,
                    fullscr=fullscreen,
                    color=self.window_color,
                    size=size,
                    monitor=monitor)

        if "framerate" in minfo:
            self.framerate = minfo["framerate"]

        self.name = self.monitor_name
        self.__dict__.update(info)
        self.window_kwargs = info
        
        
        """Open up a presentation window and measure the refresh rate."""
        stated_refresh_hz = self.framerate

        # Initialize the Psychopy window object
        win = visual.Window(**self.window_kwargs)

        # Record the refresh rate we are currently achieving
        if self.test_refresh or stated_refresh_hz is None:
            win.setRecordFrameIntervals(True)
            logging.console.setLevel(logging.CRITICAL)
            flip_time, _, _ = visual.getMsPerFrame(win)
            observed_refresh_hz = 1000 / flip_time
            print('observed_refresh_hz',observed_refresh_hz)
            
        # Possibly test the refresh rate against what we expect
        if self.test_refresh and stated_refresh_hz is not None:
            refresh_error = np.abs(stated_refresh_hz - observed_refresh_hz)
            print('refresh_error',refresh_error)
            if refresh_error > test_tol:
                msg = ("Observed refresh rate differs from expected by {:.3f} Hz"
                       .format(refresh_error))
                raise RuntimeError(msg)

        # Set the refresh rate to use in the experiment
        if stated_refresh_hz is None:
            msg = "Monitor configuration does not have refresh rate information"
            warnings.warn(msg)
            win.framerate = observed_refresh_hz
        else:
            win.framerate = stated_refresh_hz

        return win


    def run_times_to_itis(self):
        
        run_fname = op.join(op.abspath('timing'),'run' + str(int(self.run) - 1) + '.csv')
        self.intended_design = pd.read_csv(run_fname)
        
        
        timing = op.join(op.abspath('timing'),'run' + str(int(self.run) - 1) + '_timing.csv')
        timing = pd.read_csv(timing)
        self.isi_root = timing['isi1'].values
        self.isi_choice = timing['isi2'].values
        self.iti = timing['iti'].values
        
        if self.run_mode in ['experimenter','practice']: #fixed iti/isis for experimenter mode
            self.isi_root = [self.experimenter_mode_timing]*timing.shape[0]
            self.isi_choice = [self.experimenter_mode_timing]*timing.shape[0]
            self.iti = [self.experimenter_mode_timing]*timing.shape[0]

import os
import os.path as op
import pickle
from numpy.random import RandomState
import datastruct
import glob
import pandas as pd
import numpy as np
import glob

def pickle_to_df(subs):
    
    files = glob.glob(op.abspath('./data/*pkl'))
    df = []
    for f in files:
        if "+" in f:
            print('WARNING Duplicate Detected',f.split('/')[-1])
    
        if 'practice' not in f:
            #load pickle
            p_f = open(f,'rb')
            p = pickle.load(p_f)

            if p.sub in subs:
                #load subject info
                sub_data = p.run_info
                sub_data['sub'] = p.sub

                sub_data['resp'] = p.choice
                sub_data['semantic_resp'] = p.semantic_resp
                sub_data['choice_rt'] = p.choice_rt
                sub_data['semantic_rt'] = p.semantic_rt

                #remap choices
                choice = []
                resp_bin = []
                for lr, resp in zip(sub_data['left_right'], sub_data['resp']):
                    if resp == '1':
                        resp_bin.append(1)
                        if lr == 'left':
                            choice.append('Image1')
                        else:
                            choice.append('Image2')
                    elif resp == '2':
                        resp_bin.append(0)
                        if lr == 'left':
                            choice.append('Image2')
                        else:
                            choice.append('Image1')
                    else:
                        resp_bin.append(np.nan)
                        choice.append('missed')

                choice_map = {'Image1':0, 'Image2': 1, 'missed': np.NaN}
                choice_bin = [choice_map[x] for x in choice]
                sub_data['choice'] = choice
                sub_data['choice_bin'] = choice_bin
                sub_data['resp_bin'] = resp_bin
                sub_data['decision_dur'] = p.second_decision_dur
                sub_data['run_mode'] = p.run_mode
                sub_data['root_times'] = p.root_times
                sub_data['choice_times'] = p.choice_times

                sub_data['feedback_times'] = p.feedback_times
                sub_data['rew'] = p.rewards

                sub_data['isi_root'] = p.isi_root
                sub_data['isi_choice'] = p.isi_choice

                sub_data['iti'] = p.iti
                sub_data['bank'] = p.bank

                df.append(sub_data.copy())
        
    df = pd.concat(df)
    df = df.sort_values(by = ['sub','run','root_times']).reset_index()
    df = df.drop(columns = ['index','Unnamed: 0','IT_diff','V2_diff'])
    
    return df   

def correct_late_response_coding(df):
    #late responses are recorded in the experiment
    #probably best to keep those separate
    df['choice_incl_late_responses'] = df['choice']
    df['choice_bin_incl_late_responses'] = df['choice_bin']
    df['resp_bin_incl_late_responses'] = df['resp_bin']
    df['choice_rt_incl_late_responses'] = df['choice_rt']


    df.loc[np.isnan(df.rew),'choice'] = 'missed'
    df.loc[np.isnan(df.rew),'choice_bin'] = np.NaN
    df.loc[np.isnan(df.rew),'resp_bin'] = np.NaN
    df.loc[np.isnan(df.rew),'choice_rt'] = np.NaN
    
    return df
def compute_bonus(df,subs):
    df = df.set_index('sub')
    print('\nBONUSES\n')
    
    for sub in subs:
        sub_df = df.loc[sub].copy().set_index('run')
        runs = set(sub_df.index)
        rewarded = np.random.choice(list(runs))
        
        print(sub,str(sub_df.loc[rewarded,'bank'].values[0]*.5) + ' dollars')


sub_file = './subjects.txt'

if not op.exists(sub_file):
    print('\nNo subjects file! Make subjects.txt\n')
    exit()
    
subs = np.loadtxt('./subjects.txt',str)
print('\nRunning for subjects',subs,'\n')
df = pickle_to_df(subs) 
df = correct_late_response_coding(df)
compute_bonus(df,subs)

df.to_csv(op.abspath('./data/data.csv'))


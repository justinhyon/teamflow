#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10/16/2020

@author: jhyon

VERSION 1.0.0
"""
import sys
import numpy as np

# import multiprocessing.pool

# insert path to directory where JH_offline_client.py is located
path = '/Users/jasonhyon/Documents/GitHub/teamflow/src'
sys.path.insert(1, path)
from JH_realtime_client_2022 import TeamFlow

# general configurations
option = 'realtime'
savepath = '/Users/jasonhyon/Documents/GitHub/teamflow/misc/merge_test/rt'
blocksize_sec = 5  # number of seconds per segment
units = 'uv'  # v for volts, mv for millivolts, uv for microvolts, Mv for megavolts

plotpref = 'experiment'  # use either 'participant'(teamflow score plot), 'experiment'(detailed plot), 'both', or 'none' to
# toggle showing the plots
ex_windowsize = (24, 12)  # size of the figures
sub_windowsize = (36, 12)  # size of the figures
ex_plot_dims = (5, 4)  # The dimensions of the plot grid to be used for the experimenter plot. Be sure to count total
# number of required plots, or desired plots will not be rendered
sub_plot_dims = (2, 3)  # The dimensions of the plot grid to be used for the subject plot. Be sure to count total
# number of required plots, or desired plots will not be rendered
saving = False  # True or False. toggle saving the plots. Must create a folder called "TF_figures" in path directory
# (line 13) before running. there is currently a bug that prevents the team flow scores plot from saving
badchans1 = ['A32', 'B2']  # bad channels
badchans2 = []
nchansparticipant = 128  # number of channels per particiapnt
removefirstsample = True
TrigChan = 256  # python begins numbering from 0, so this is the channel number of the stim channel - 1 (not the name)
numparticipants = 2
channelnames = []
for letter in ['A', 'B', 'C', 'D']:
    for num in range(1, 33):
        channelnames.append(letter + str(num))
# channelnames.append('STIM 001')


# configurations for realtime mode (ignored in offline mode)
exp_name = 'test_2'
dataport = 1972
n_skipped_segs = 1  # max number of segments to skip in between 2 processed segments due to runtime
wait_segs = 2  # How many segments worth of time (blocksize_sec) to wait for new data before quitting the pipeline. does
# not apply to the initial wait for first segment to arrive
delay = .01  # how long to wait before checking again for new samples in the buffer

# configurations for offline mode (ignored in realtime mode)
filepath = '/Users/jasonhyon/Desktop/JoinedData/170719_TRIAL2__EM_MD.set'  # path to the  bdf data file
fsample = 256  # samples per second

function_dict = {}
# ----------------aep configurations----------------- erp

function_dict['aep1'] = {
    # subject 1
    'values_aep': [],
    'channelofint': [1, 2, 3, 33, 34, 52, 65, 66, 87, 97, 98, 110, 111, 112],
    'epoeventval': 5,  # stim channel event value desired
    'pretrig': .3,  # seconds before event
    'posttrig': .5,  # seconds after event
    'plotwv': 'experiment',
    'plotidx': 'experiment'
}
function_dict['aep2'] = {
    # subject 2
    'values_aep': [],
    'channelofint': [129, 130, 131, 161, 162, 180, 193, 194, 215, 225, 226, 238, 239, 240],
    'epoeventval': 5,
    'pretrig': .3,
    'posttrig': .5,
    'plotwv': 'experiment',
    'plotidx': 'experiment'
}

# -----------------plv configurations (unused since MNE does everything)----------------- interbrain connectivity ibc
num_plvsimevents = 5  # number of simulated events for each PLV segment
channelofint_plv = 0
frqofint = 0
function_dict['plv'] = {
    'plot_option': (1,2), # either tuple or one of 'experiment' or 'participant'. if tuple specified, intrabrain plv
                            # indexes will be plotted for the participants desired. if 'experiment' or 'participant' is
                            # specified, an average of all the intrabrain plvs is plotted
    # interbrain settings must come first
    'values_inter': [],
    'plot_matrix': 'experiment',
    'index_inter': 'experiment',

    'values_intra1': [],
    'index_intra1': 'experiment',

    'values_intra2': [],
    'index_intra2': 'experiment',

    # 'values_intra3': [],
    # 'index_intra3': 'experiment',
    #
    # 'values_intra4': [],
    # 'index_intra4': 'experiment',

}

# --------------psd configurations. T= temporal, F=frontal, A=occipital. 1 and 2 are the participant #s----------------
function_dict['psd1'] = {
    'values_band1': [],
    'channelofint_band1': [116, 117, 119, 126],  # [117, 118, 120, 127] actual channels of interest subject 1
    'foilow_band1': 30,
    'foihigh_band1': 119,
    'plotwv_band1': 'experiment',
    'plotidx_band1': 'experiment',

    'values_band2': [],
    'channelofint_band2': [116, 117, 119, 126],  # [117, 118, 120, 127] actual channels of interest subject 1
    'foilow_band2': 12,
    'foihigh_band2': 29,
    'plotwv_band2': 'experiment',
    'plotidx_band2': 'experiment',

    'values_band3': [],
    'channelofint_band3': [116, 117, 119, 126],  # [117, 118, 120, 127] actual channels of interest subject 1
    'foilow_band3': 7,
    'foihigh_band3': 11,
    'plotwv_band3': 'experiment',
    'plotidx_band3': 'experiment',
}

function_dict['psd2'] = {
    'values_band1': [],
    'channelofint_band1': [244, 245, 247, 254],  # [117, 118, 120, 127] actual channels of interest subject 1
    'foilow_band1': 30,
    'foihigh_band1': 119,
    'plotwv_band1': 'experiment',
    'plotidx_band1': 'experiment',

    'values_band2': [],
    'channelofint_band2': [244, 245, 247, 254],  # [117, 118, 120, 127] actual channels of interest subject 1
    'foilow_band2': 12,
    'foihigh_band2': 29,
    'plotwv_band2': 'experiment',
    'plotidx_band2': 'experiment',

    'values_band3': [],
    'channelofint_band3': [244, 245, 247, 254],  # [117, 118, 120, 127] actual channels of interest subject 1
    'foilow_band3': 7,
    'foihigh_band3': 11,
    'plotwv_band3': 'experiment',
    'plotidx_band3': 'experiment',
}

function_dict['flow'] = {
            'values_Intra 1': [],
            'values_Intra 2': [],
            'values_Inter': []
        }

channelofint_psdT1 = [116, 117, 119, 126]  # [245, 246, 248, 255] actual channels of interest subject 2
foillowT1 = 30
foihighT1 = 119
channelofint_psdT2 = [244, 245, 247, 254]  # [245, 246, 248, 255] actual channels of interest subject 2
foillowT2 = 30
foihighT2 = 119
# Beta
channelofint_psdF1 = [116, 117, 119, 126]  # [117, 118, 120, 127] actual channels of interest subject 1
foillowF1 = 12
foihighF1 = 29
channelofint_psdF2 = [244, 245, 247, 254]  # [245, 246, 248, 255] actual channels of interest subject 2
foillowF2 = 12
foihighF2 = 29

# Alpha
channelofint_psdA1 = [116, 117, 119, 126]  # [117, 118, 120, 127] actual channels of interest subject 1
foillowA1 = 7
foihighA1 = 11
channelofint_psdA2 = [244, 245, 247, 254]  # [245, 246, 248, 255] actual channels of interest subject 2
foillowA2 = 7
foihighA2 = 11

if __name__ == '__main__':
    TF = TeamFlow(path, savepath, dataport, ex_windowsize, sub_windowsize, delay, plotpref, saving, TrigChan, )

    TF.master_control(filepath=filepath,
                      badchans=[badchans1, badchans2],
                      fsample=fsample,
                      nchansparticipant=nchansparticipant,
                      trigchan=TrigChan,
                      featurenames=['Gamma1', 'Beta1', 'Alpha1', 'Gamma2', 'Beta2', 'Alpha2'],
                      channelofints=[channelofint_psdT1, channelofint_psdF1, channelofint_psdA1,
                                     channelofint_psdT2, channelofint_psdF2, channelofint_psdA2],
                      foilows=[foillowT1, foillowF1, foillowA1],
                      foihighs=[foihighT1, foihighF1, foihighA1],
                      blocksize_sec=blocksize_sec,
                      num_plvsimevents=num_plvsimevents,  # [[channelofint_aep1, epoeventval1, pretrig1, posttrig1],
                      # [channelofint_aep2, epoeventval2, pretrig2, posttrig2]],
                      option=option,
                      delay=delay,
                      units=units,
                      remfirstsample=removefirstsample,
                      exp_name=exp_name,
                      n_skipped_segs=n_skipped_segs,
                      wait_segs=wait_segs,
                      function_dict=function_dict,
                      numparticipants=numparticipants,
                      ex_plot_matrix=np.zeros(ex_plot_dims),
                      sub_plot_matrix=np.zeros(sub_plot_dims),
                      channelnames=channelnames),

    # For PSD:
    # List of FOI low and high must be the same length
    # Length of channels list must be an integer multiple of FOI low/high list length
    # Put all features related to the same subject together, in the same feature order
    # For AEP:
    # AEPs should be stored in a list of lists. The wrapper lists should correspond to each of the participants.
    # the number of wrapper lists should equal the number of participants. The nested list should contain data
    # corresponding to a single participant

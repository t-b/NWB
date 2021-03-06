# encoding: utf-8

import sys
sys.path.append('../')
from AllenSDK.allensdk.ephys.ephys_extractor import EphysSweepFeatureExtractor
import pyabf
import numpy as np
# from neo import io as nio


# pyabf - Updated version (2.1.7)
#
# Iterate through the sweeps in the ABF file to access raw data for each sweep.
# Sampling rate is fixed for White Noise experiments, but need to become variable.
# Raw data is used with the Allen Institute's analysis functions

# Data already in units of pA and mV - no conversion needed

abf = pyabf.ABF(r"C:\NWB\Files\Human_tissue\Epilepsy cases\April 17, 2018\Cell 3\Gain 40\18417026.abf")

for i in range(abf.sweepCount):
    abf.setSweep(i)
    # print("sweep data (ADC):", abf.sweepY)
    # print("sweep command (DAC):", abf.sweepC)
    # print("sweep times (seconds):", abf.sweepX)

    response = abf.sweepY
    stimulus = abf.sweepC

    sampling_rate = 10e4

    t = np.arange(0, len(response)) * (1.0 / sampling_rate)

    sweep_ext = EphysSweepFeatureExtractor(t=t, v=response, i=stimulus)
    try:
        sweep_ext.process_spikes()
    except:
        print("Failure: %d th sweep" % i)

    print("Sweep %d:" % i)
    print("Avg spike threshold: %.01f mV" % sweep_ext.spike_feature("threshold_v").mean())
    print("Avg spike width: %.02f ms" % (1e3 * np.nanmean(sweep_ext.spike_feature("width"))))



# neo (as used by Prajay prior to pyabf)

# fpath = r"C:\NWB\Files\Human_tissue\Epilepsy cases\April 17, 2018\Cell 3\Gain 40\18417026.abf"
# f = "18417026"
# fpath = "/Users/youngseo/Documents/Research/nwb/18426011.abf"
# with open(fpath, encoding='0xFF'):
#     fpath = fpath
# f = "18426011"

# Load up abf file - legacy nio importer (less functionality than pyABF and prone to breaking)
# h = {}
# si = {}  # sampling intervals for each cell in us
# d = {}
# V = {}
# I = {}
#
# a = nio.AxonIO(filename=fpath)
# bl = a.read_block(lazy=False)
# # - .segments represent sweeps (one segment = one sweep)
# # - .analogsignals for each segment: numpy array of voltage recordings and current input, length of recording block, and sampling rate
# iclamp = 0  # channel 4 as voltage channel
# current_in = 1  # channel 14 as command channel
# V[f] = []  # numpy array of voltage recordings for all sweeps/segments - rows = sweeps, columns = data
# for i in range(0, len(bl.segments)):
#     a = bl.segments[i].analogsignals[iclamp].__array__().tolist()
#     V[f].append([item for x in a for item in x])
# V[f] = np.array(V[f])
# I[f] = []  # numpy array of stimulus for all sweeps/segments - rows = sweeps, columns = data
# for i in range(0, len(bl.segments)):
#     a = bl.segments[i].analogsignals[current_in].__array__().tolist()
#     I[f].append([item for x in a for item in x])
# I[f] = np.array(I[f])
#
# print(V[f])
# print(I[f])
#
# # save data block for each cell
# d[f] = bl
#
# for i in range(len(V[f])):
#     stimulus = I[f][i] * 1e12
#     response = V[f][i] * 1e3
#
#     sampling_rate = 10e4
#
#     t = np.arange(0, len(response)) * (1.0 / sampling_rate)
#
#     sweep_ext = EphysSweepFeatureExtractor(t=t, v=response, i=stimulus)
#     try:
#         sweep_ext.process_spikes()
#     except:
#         print("Failure: %s th sweep" % i)
#
#     print("Avg spike threshold: %.01f mV" % sweep_ext.spike_feature("threshold_v").mean())
#     print("Avg spike width: %.02f ms" % (1e3 * np.nanmean(sweep_ext.spike_feature("width"))))






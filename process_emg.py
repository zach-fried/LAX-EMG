import math
import numpy as np
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from helpers import import_MVC, import_dynamic, parse_emg

# import MVC files
emg_MVC_RQuad = import_MVC('LX1511MVCRQuad01.xlsx')
emg_MVC_RHam = import_MVC('LX1511MVCRHam01.xlsx')
emg_MVC_LQuad = import_MVC('LX1511MVCLQuad01.xlsx')
emg_MVC_LHam = import_MVC('LX1511MVCLHam01.xlsx')

# import dynamic trial
emg_dynamic = import_dynamic('Trimmed_LX1511eT08R1.xlsx')

# parse R Rectus data and time vector from trial for testing
emg_MVC_dict, emg_dynamic_dict, time = parse_emg(emg_MVC_RQuad, emg_MVC_RHam, emg_MVC_LQuad, emg_MVC_LHam, emg_dynamic)

"""
# plot raw data
fig_raw = plt.figure(dpi=200)
axes_raw = fig_raw.add_axes([0.1,0.1,0.8,0.8])
axes_raw.plot(time_dynamic, emg_RRec_MVC, 'b')
axes_raw.plot(time_dynamic, emg_RRec_dynamic, 'r')
axes_raw.set_title('Raw Data')
plt.show()
"""

# Define static variables for filter design
sample_rate = 4800
nyq = sample_rate*0.5
cutoff_high_pass = 20
cutoff_low_pass = 5

# high pass filter data
b, a = signal.butter(6, (cutoff_high_pass*1.116)/nyq, btype='highpass')

emg_MVC_high = dict()
emg_dyn_high = dict()

emg_MVC_high_sum = dict()
emg_dyn_high_sum = dict()

emg_MVC_high_mean = dict()
emg_dyn_high_mean = dict()

for k in emg_MVC_dict:
    emg_MVC_high[k] = signal.filtfilt(b, a, emg_MVC_dict[k])
    emg_dyn_high[k] = signal.filtfilt(b, a, emg_dynamic_dict[k])

for k in emg_MVC_high:
    emg_MVC_high_sum[k] = sum(emg_MVC_high[k])
    emg_dyn_high_sum[k] = sum(emg_dyn_high[k])

for k in emg_MVC_high_sum:
    emg_MVC_high_mean[k] = emg_MVC_high_sum[k]/len(emg_MVC_high[k])
    emg_dyn_high_mean[k] = emg_dyn_high_sum[k]/len(emg_dyn_high[k])

#emg_MVC_high_mean = sum(emg_MVC_high.values())
#emg_dyn_high_mean = sum(emg_dyn_high.values())

# print(emg_MVC_high_mean)
# print(emg_dyn_high_mean)

for k in emg_MVC_high:
    emg_MVC_high[k] = emg_MVC_high[k] - emg_MVC_high_mean[k]
    emg_dyn_high[k] = emg_dyn_high[k] - emg_dyn_high_mean[k]

# full wave rectify data
emg_MVC_rect = dict()
emg_dyn_rect = dict()

# SOMETHING IS GOING WRONG HERE - OUTPUT FILE CONTAINS NEGATIVE
# VALUES DESPITE FULL WAVE RECTIFICATION
for k in emg_MVC_dict:
    emg_MVC_rect[k] = abs(emg_MVC_high[k])
    emg_dyn_rect[k] = abs(emg_dyn_high[k])

# low pass filter data to calculate linear envelope
d, c = signal.butter(4, (cutoff_low_pass*1.116)/nyq, btype='lowpass')

# print(d, c)

emg_MVC_env = dict()
emg_dyn_env = dict()

# Testing removal of the mean of the signal to correct DC offset
for k in emg_MVC_dict:
    emg_MVC_env[k] = signal.filtfilt(d, c, emg_MVC_rect[k])
    emg_dyn_env[k] = signal.filtfilt(d, c, emg_dyn_rect[k])

"""
# plot linear envelopes
fig_env = plt.figure(dpi=200)
axes_env = fig_env.add_axes([0.1,0.1,0.8,0.8])
axes_env.plot(time, emg_MVC_env['LRec'], 'b')
axes_env.plot(time, emg_dyn_env['LRec'], 'r')
axes_env.set_title('Linear Envelope')
plt.show()
"""

# normalize dynamic trial to MVC
emg_dyn_norm = dict()

for k in emg_MVC_dict:
    emg_dyn_norm[k] = (emg_dyn_env[k] / emg_MVC_env[k].mean()) * 100

# if negative, add min value to all values to correct DC offset
for k in emg_dyn_norm:
    if min(emg_dyn_norm[k]) < 0:
        emg_dyn_norm[k] = emg_dyn_norm[k] + abs(float(min(emg_dyn_norm[k])))

emg_final = pd.DataFrame(emg_dyn_norm)

muscles = ['RVM', 'RRec', 'RVL', 'RSemi', 'RBic', 'LVM', 'LRec',
'LVL', 'LSemi', 'LBic']

# plot normalized data as percentage of MVC NOT WORKING

fig_norm, axes_norm = plt.subplots(nrows = 2, ncols = 5, dpi=200)

i = 0
for r in range(0, len(axes_norm[0,:])):
    axes_norm[0,r].plot(time, emg_final[muscles[i]])
    axes_norm[0,r].set_title(f'{muscles[i]}')
    i+= 1
for c in range(0, len(axes_norm[1,:])):
    axes_norm[1,c].plot(time, emg_final[muscles[i]])
    axes_norm[1,c].set_title(f'{muscles[i]}')
    i += 1

plt.tight_layout()
plt.show()

# plot single normalized curve
"""
fig_norm = plt.figure(dpi=200)
axes_norm = fig_norm.add_axes([0.1,0.1,0.8,0.8])
axes_norm.plot(time, emg_dyn_norm['LRec'], 'c')
plt.show()
"""

emg_final.to_excel('test.xlsx')
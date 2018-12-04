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
cutoff_low_pass = 20

# high pass filter data
b, a = signal.butter(4, (cutoff_high_pass*1.116)/nyq, btype='highpass')

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

pd.DataFrame(emg_MVC_high).to_excel('emg_MVC_high.xlsx')

"""
# plot high pass filtered data
fig_high = plt.figure(dpi=200)
axes_high = fig_high.add_axes([0.1,0.1,0.8,0.8])
axes_high.plot(time, emg_MVC_high['LVM'], 'b')
axes_high.plot(time, emg_dyn_high['LVM'], 'r')
axes_high.set_title('High pass')
plt.show()
"""

# full wave rectify data
emg_MVC_rect = dict()
emg_dyn_rect = dict()

# SOMETHING IS GOING WRONG HERE - OUTPUT FILE CONTAINS NEGATIVE
# VALUES DESPITE FULL WAVE RECTIFICATION
for k in emg_MVC_dict:
    emg_MVC_rect[k] = abs(emg_MVC_high[k])
    emg_dyn_rect[k] = abs(emg_dyn_high[k])

# Trying to track down negative values
pd.DataFrame(emg_MVC_rect).to_excel('emg_MVC_rect.xlsx')
pd.DataFrame(emg_dyn_rect).to_excel('emg_dyn_rect.xlsx')

"""
fig_rect = plt.figure(dpi=200)
axes_rect = fig_rect.add_axes([0.1,0.1,0.8,0.8])
axes_rect.plot(time, emg_MVC_rect['LVM'], 'b')
axes_rect.plot(time, emg_dyn_rect['LVM'], 'r')
axes_rect.set_title('Rectified')
plt.show()
"""

# low pass filter data to calculate linear envelope
d, c = signal.butter(4, (cutoff_low_pass*1.116)/nyq, btype='lowpass')

# print(d, c)

emg_MVC_env = dict()
emg_dyn_env = dict()

# Testing removal of the mean of the signal to correct DC offset
for k in emg_MVC_dict:
    emg_MVC_env[k] = signal.filtfilt(d, c, emg_MVC_rect[k])
    emg_dyn_env[k] = signal.filtfilt(d, c, emg_dyn_rect[k])

# Trying to track down negative values
pd.DataFrame(emg_MVC_env).to_excel('emg_MVC_env.xlsx')
pd.DataFrame(emg_dyn_env).to_excel('emg_dyn_env.xlsx')


# plot linear envelopes
fig_env = plt.figure(dpi=200)
axes_env = fig_env.add_axes([0.1,0.1,0.8,0.8])
axes_env.plot(time, emg_MVC_env['RVL'], 'b')
axes_env.plot(time, emg_dyn_env['RVL'], 'r')
axes_env.set_title('Linear Envelope')
plt.show()

# normalize dynamic trial to MVC
emg_dyn_norm = dict()

for k in emg_MVC_dict:
    emg_dyn_norm[k] = (emg_dyn_env[k] / emg_MVC_env[k]) * 100

"""
# plot normalized data as percentage of MVC
fig_norm, axes_norm = plt.subplots(2, 5)
#axes_norm = fig_norm.add_axes([0.1,0.1,0.8,0.8])
for row, k in zip(axes_norm, emg_dyn_norm.keys()):
    for col in row:
        col.plot(time, emg_dyn_norm[k])
#axes_norm.plot(time, emg_dyn_norm['RVM'], time, emg_dyn_norm['RRec'], time, emg_dyn_norm['RVL'], time, emg_dyn_norm['RSemi'], time, emg_dyn_norm['RBic'], time, emg_dyn_norm['LVM'], time, emg_dyn_norm['LRec'], time, emg_dyn_norm['LVL'], time, emg_dyn_norm['LSemi'], time, emg_dyn_norm['LBic'], 'c')
plt.show()
"""

pd.DataFrame(emg_dyn_norm).to_excel('test.xlsx')
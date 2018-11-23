import math
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
cutoff_high = 30
cutoff_low = 4

# high pass filter data
b, a = signal.butter(4, cutoff_high/nyq, btype='highpass')

emg_MVC_high = dict()
emg_dyn_high = dict()

for k in emg_MVC_dict:

    emg_MVC_high[k] = signal.filtfilt(b, a, emg_MVC_dict[k])
    emg_dyn_high[k] = signal.filtfilt(b, a, emg_dynamic_dict[k])

"""
# plot high pass filtered data
fig_high = plt.figure(dpi=200)
axes_high = fig_high.add_axes([0.1,0.1,0.8,0.8])
axes_high.plot(time_dynamic, emg_RRec_MVC_high, 'b')
axes_high.plot(time_dynamic, emg_RRec_dyn_high, 'r')
axes_high.set_title('High pass')
plt.show()
"""

# full wave rectify data
emg_MVC_rect = dict()
emg_dyn_rect = dict()

for k in emg_MVC_dict:
    emg_MVC_rect[k] = abs(emg_MVC_high[k])
    emg_dyn_rect[k] = abs(emg_dyn_high[k])

# low pass filter data to calculate linear envelope
d, c = signal.butter(4, cutoff_low/nyq, btype='lowpass')

emg_MVC_env = dict()
emg_dyn_env = dict()

for k in emg_MVC_dict:
    emg_MVC_env[k] = signal.filtfilt(d, c, emg_MVC_rect[k])
    emg_dyn_env[k] = signal.filtfilt(d, c, emg_dyn_rect[k])
"""
# plot linear envelopes
fig_env = plt.figure(dpi=200)
axes_env = fig_env.add_axes([0.1,0.1,0.8,0.8])
axes_env.plot(time, emg_MVC_env['RRec'], 'b')
axes_env.plot(time, emg_dyn_env['RRec'], 'r')
axes_env.set_title('Linear Envelope')
plt.show()
"""
# normalize dynamic trial to MVC
emg_dyn_norm = dict()

for k in emg_MVC_dict:
    emg_dyn_norm[k] = (emg_dyn_env[k] / emg_MVC_env[k]) * 100
"""
# plot normalized data as percentage of MVC
fig_norm = plt.figure(dpi=200)
axes_norm = fig_norm.add_axes([0.1,0.1,0.8,0.8])
axes_norm.plot(time, emg_dyn_norm['RRec'], 'c')
axes_norm.set_title('Normalized Data?')
plt.show()
"""

pd.DataFrame(emg_dyn_norm).to_excel('test.xlsx')
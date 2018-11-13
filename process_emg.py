import math
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from import_emg import import_MVC, import_dynamic

# import MVC file
emg_MVC = import_MVC('LX1511MVCRQuad01.xlsx')

# import dynamic trial
emg_dynamic = import_dynamic('Trimmed_LX1511eT08R1.xlsx')

# parse R Rectus data and time vector from trial for testing
time_dynamic = emg_dynamic['File_Type:'][10:]
emg_RRec_MVC = emg_MVC['Unnamed: 20'][10:(len(time_dynamic)+10)]
emg_RRec_dynamic = emg_dynamic['Unnamed: 20'][10:]

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
b_MVC, a_MVC = signal.butter(4, cutoff_high/nyq, btype='highpass')
emg_RRec_MVC_high = signal.filtfilt(b_MVC, a_MVC, emg_RRec_MVC)

b_dyn, a_dyn = signal.butter(4, cutoff_high/nyq, btype='highpass')
emg_RRec_dyn_high = signal.filtfilt(b_dyn, a_dyn, emg_RRec_dynamic)

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
emg_RRec_MVC_rect = abs(emg_RRec_MVC_high)
emg_RRec_dyn_rect = abs(emg_RRec_dyn_high)

# low pass filter data to calculate linear envelope
d_MVC, c_MVC = signal.butter(4, cutoff_low/nyq, btype='lowpass')
emg_RRec_MVC_env = signal.filtfilt(d_MVC, c_MVC, emg_RRec_MVC_rect)

d_dyn, c_dyn = signal.butter(4, cutoff_low/nyq, btype='lowpass')
emg_RRec_dyn_env = signal.filtfilt(d_dyn, c_dyn, emg_RRec_dyn_rect)

# plot linear envelopes
fig_env = plt.figure(dpi=200)
axes_env = fig_env.add_axes([0.1,0.1,0.8,0.8])
axes_env.plot(time_dynamic, emg_RRec_MVC_env, 'b')
axes_env.plot(time_dynamic, emg_RRec_dyn_env, 'r')
axes_env.set_title('Linear Envelope')
plt.show()

# normalize dynamic trial to MVC
emg_RRec_dyn_norm = (emg_RRec_dyn_env / emg_RRec_MVC_env) * 100

# plot normalized data as percentage of MVC
fig_norm = plt.figure(dpi=200)
axes_norm = fig_norm.add_axes([0.1,0.1,0.8,0.8])
axes_norm.plot(time_dynamic, emg_RRec_dyn_norm, 'c')
axes_norm.set_title('Normalized Data?')
plt.show()
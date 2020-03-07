# AGH UST Medical Informatics 03.2020
# Lab 1 : ECG (Electrocardiography)
# Data sampling frequency : 100 Hz

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# params
max_samples = 1000
sampling_frequency = 100

# read data
ecg = np.zeros(max_samples)
with open('./data/ecg.data') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    idx = 0
    for row in csv_reader:
        if idx > 0 and idx < max_samples:
            ecg[idx] = float(row[0])
        idx = idx + 1

# find peaks
peaksAll, _ = find_peaks(ecg)
print(peaksAll)

# heart rate
R_peaks = list(filter(lambda x: ecg[x] > 0.3, peaksAll))
time_interval = (R_peaks[-1] - R_peaks[0]) / (60 * sampling_frequency)
R_peaks_in_time_interval = len(R_peaks) - 1
average_heart_rate =  R_peaks_in_time_interval / time_interval
print("Average heart rate is:", average_heart_rate)

peaks_pairs_time_intervals = np.diff(R_peaks) / (60 * sampling_frequency)
tmp_heart_rates = 1 / peaks_pairs_time_intervals
print("Heart rates for each pair of beats:")
print(tmp_heart_rates)

# filter
window_size = 6
ecg_filt = np.convolve(ecg, np.full(window_size, 1), mode='valid') / window_size

# PRT peaks
peaksPRT, _ = find_peaks(ecg_filt)
r_peaks_indices = np.reshape(np.argwhere(ecg_filt[peaksPRT] > 0.15), -1)
p_peaks = peaksPRT[r_peaks_indices - 1]
r_peaks = peaksPRT[r_peaks_indices]
t_peaks = peaksPRT[r_peaks_indices + 1]
peaksPRT = np.concatenate([p_peaks, r_peaks, t_peaks])

# plot heart rate
plt.figure(figsize=(15,8))
plt.plot(tmp_heart_rates)
plt.show()

# plot ECG
plt.figure(figsize=(15,8))
plt.plot(ecg, '#999999')
# plt.plot(peaksAll, ecg[peaksAll], "rx")
# plot PRT peaks
plt.plot(ecg_filt, 'g')
plt.plot(peaksPRT, ecg_filt[peaksPRT], "rx")
plt.show()



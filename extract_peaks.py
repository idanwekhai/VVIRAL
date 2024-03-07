import os
import re
import glob
import math
from collections import defaultdict
from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths, savgol_filter, convolve, peak_prominences
from peak_metrics import *
from utils import *


CSVs = []
for root, dirs, files in os.walk("Affinity Data"):
    for file in files:
        if file.endswith(".csv"):
             CSVs.append(os.path.join(root, file))


frame = {'file': [], 'Tailing Factor': [], 'Peak Assymetry': [], 'No. Theoretical Plates': [], 'Area (mAU*ml)':[], 'Height':[], 'No. Elutions': []}

count = 0
errors = []
for csv in CSVs:
    name = csv.split('/')[-1][:-4]
    resin, serotype = get_resin_and_serotype(name)
    if resin == 'U':
        resin = get_resin(name)
    if serotype == 'U':
        serotype = csv.split('/')[1]
    # print(csv)
    try:
        df = pd.read_csv(csv, skiprows = [0,1], delimiter='\t', encoding='utf_16', on_bad_lines='skip', low_memory=False)
    except Exception as e:
        print(e, csv)

    try:

        # column_wash_idx, cip_idx = get_elution_and_cip_idx(df)
        start_idx, stop_idx, two_elutions = get_start_stop_idx(df)

        data = load_useful_data(df)

        if start_idx != None and stop_idx != None:
            count += 1
            start = df[data['Run Log']].loc[start_idx].values[0]
            stop = df[data['Run Log']].loc[stop_idx].values[0]

            
            cols = df[data['UV_280']].columns
            volume = df[data['UV_280']][cols[0]]
            uv_280 = df[data['UV_280']][cols[1]]

            volume = volume.apply(lambda x: 0 if x < start else x)
            volume = volume.apply(lambda x: 0 if x > stop else x)
            volume = volume.loc[volume > 0]

            uv_280 = uv_280[volume.index]
            uv_280  = uv_280.apply(lambda x: 0 if x < 0 else x)
            uv_280 = uv_280.loc[uv_280 > 0]
            uv_280.dropna(inplace=True)
            volume = volume.loc[uv_280.index]
            uv_280.reset_index(drop=True, inplace=True)
            volume.reset_index(drop=True, inplace=True)
            # mid_absorbance = max(uv_280) / 2
            eighty_five_percent_of_max_adsorbance = max(uv_280) * 0.85
            peaks, info = find_peaks(uv_280, height=eighty_five_percent_of_max_adsorbance, width=15)
            results_half = peak_widths(uv_280, peaks, rel_height=0.5)
            results_full = peak_widths(uv_280, peaks, rel_height=1)
            results_five_pec = peak_widths(uv_280, peaks, rel_height=0.95)
            results_ten_pec = peak_widths(uv_280, peaks, rel_height=0.9)
            prominences = peak_prominences(uv_280, peaks)[0]
            contour_heights = uv_280[peaks] - prominences

            half_width = query_line(volume, results_half[1:])
            full_width = query_line(volume, results_full[1:])
            ten_percent_width = query_line(volume, results_ten_pec[1:])
            five_percent_width = query_line(volume, results_five_pec[1:])
            frame['file'].append(name)
            frame['Tailing Factor'].append(tailing_factor(peaks, results_five_pec[1:]))
            frame['Peak Assymetry'].append(peak_assymetry(peaks, results_ten_pec[1:]))
            frame['No. Theoretical Plates'].append(number_of_theoretical_plates(volume, peaks, results_half[1:]))
            frame['Area (mAU*ml)'].append(area(volume, peaks, results_full[1:], prominences))
            frame['Height'].append(peak_height(peaks, prominences))
            if two_elutions == True:
                frame['No. Elutions'].append(2)
            else:
                frame['No. Elutions'].append(1)
            # show_peaks(name, uv_280, volume, peaks, half_width, contour_heights)
    except Exception as e:
        print(e, csv)
data = pd.DataFrame(frame)
data.to_csv('peak_metrics.csv', index=False)


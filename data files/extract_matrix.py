import os
import re
import glob
from tqdm import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import *

CSVs = []
for root, dirs, files in os.walk("Affinity Data"):
    for file in files:
        if file.endswith(".csv"):
             CSVs.append(os.path.join(root, file))


frame = {'resin': [], 'serotype': [], 'file': [], 'Column Volume (mL)':[], 'Pure':[], 'Blank':[],
         'Elution pH': [],'Wash pH': [],'Equlibration pH': [],'Elution Conductivity': [],
         'Wash Conductivity': [],'Equilibration Conductivity': [], 'Sample Volume (mL)':[],
         'System Flowrate Elution (CV/h)': [], 'Sample Flowrate Elution (CV/h)': []}
for csv in CSVs:
    name = csv.split('/')[-1][:-4]
    resin, serotype = get_resin_and_serotype(name)
    if resin == 'U':
        resin = get_resin(name)
    if serotype == 'U':
        serotype = csv.split('/')[1]
    pure = is_pure(name)
    col_vol = get_column_volume(name)
    blank = is_blank(name)
    # print(csv)
    try:
        df = pd.read_csv(csv, skiprows = [0,1], delimiter='\t', encoding='utf_16', on_bad_lines='skip', low_memory=False)
        data_dict = load_useful_data(df)
    except Exception as e:
        print(e, csv)
    
    try:
        elution_ph, elution_cond = get_ph_and_cond_at_elution(df, data_dict)
        wash_ph, wash_cond = get_ph_and_cond_at_wash(df, data_dict)
        sample_flow, system_flow = get_sample_and_sytem_flow_rate_at_elution(df, data_dict)
        equilibration_ph, equilibration_cond = get_ph_and_cond_at_equilibration(df, data_dict)
        sample_volume = get_sample_volume(df, data_dict)
        frame['resin'].append(resin)
        frame['serotype'].append(serotype)
        frame['file'].append(name)
        frame['Pure'].append(pure)
        frame['Blank'].append(blank)
        frame['Column Volume (mL)'].append(col_vol[:-2])
        frame['Elution pH'].append(elution_ph)
        frame['Wash pH'].append(wash_ph)
        frame['Equlibration pH'].append(equilibration_ph)
        frame['Elution Conductivity'].append(elution_cond)
        frame['Wash Conductivity'].append(wash_cond)
        frame['Equilibration Conductivity'].append(equilibration_cond)
        frame['Sample Volume (mL)'].append(sample_volume)
        frame['System Flowrate Elution (CV/h)'].append(system_flow)
        frame['Sample Flowrate Elution (CV/h)'].append(sample_flow)
    except Exception as e:
        print(e, csv)

data = pd.DataFrame(frame)
data[['Column Diameter (mm)', 'Coulmn Height (cm)']] = 'U'


for i in range(len(data)):
    if data['resin'][i] == 'U' and (data['serotype'][i] in ['AAV2', 'AAV6', 'AAV9', 'AAV9_with_LigaGuard']):
        # data['resin'][i] = 'AAVX'
        data.loc[i, 'resin'] = 'AAVX'

for i in range(len(data)):
    if data['Column Volume (mL)'][i] == '':
        data.loc[i, ['Coulmn Height (cm)', 'Column Diameter (mm)', 'Column Volume (mL)']] = [2.55, 5, 0.5]

for i in range(len(data)):
    if float(data['Column Volume (mL)'][i]) in [3.3, 4.0]:
        data.loc[i, 'Column Diameter (mm)'] = 10
        if data['Column Volume (mL)'][i] != 'U' and data['Coulmn Height (cm)'][i] != '':
            height = (float(data['Column Volume (mL)'][i])*1000)/(np.pi*((10/2)**2))
            data.loc[i,'Coulmn Height (cm)'] = round(height/10, 2)
    elif float(data['Column Volume (mL)'][i]) == 0.5:
        data.loc[i, 'Column Diameter (mm)'] = 5
        data.loc[i,'Coulmn Height (cm)'] = 2.55

data.to_csv('affinity_data.csv', index=False)
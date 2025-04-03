import os
import pandas as pd
from utils_xlsx import *

folder = '/home/kelidan/VVIRAL/data_dump/BTEC_Ufol/Gene Therapy Results'
folder_name = folder.split('/')[-1]

all_csvs = []
for root, dirs, files in os.walk(f"{folder}"):
    for file in files:
        if file.endswith(".xlsx"):
            all_csvs.append(os.path.join(root, file))

frame = {'resin': [], 'serotype': [], 'file': [], 'Pure':[], 'Blank':[],
         'Elution pH': [],'Wash pH': [],'Equlibration pH': [],'Elution Conductivity': [],
         'Wash Conductivity': [],'Equilibration Conductivity': [], 'Sample Volume (mL)':[],
         'System Flowrate Elution (CV/h)': [], 'Sample Flowrate Elution (CV/h)': [], 'ChromID': [], 'Column Volume (mL)': [], 
         'Retention Time (min)': [], 'Sample flowrate (CV/h)': []}
for csv in all_csvs:
    name = csv.split('/')[-1][:-5]
    resin, serotype = get_resin_and_serotype(name)
    if serotype == 'U':
        serotype = csv.split('/')[-2]
    pure = is_pure(name)
    # col_vol = get_column_volume(name)
    blank = is_blank(name)
    # print(csv)
    try:
        df = pd.read_excel(csv,skiprows = [0])
        data_dict = load_useful_data(df)
    except Exception as e:
        print(e, csv)

    try:
        elution_ph, elution_cond = get_ph_and_cond_at_elution(df, data_dict)
        wash_ph, wash_cond = get_ph_and_cond_at_wash(df, data_dict)
        sample_flow, system_flow = get_sample_and_sytem_flow_rate_at_elution(df, data_dict)
        equilibration_ph, equilibration_cond = get_ph_and_cond_at_equilibration(df, data_dict)
        sample_volume = get_sample_volume(df, data_dict)
        chrom_id = get_chrom_id(df, data_dict)
        column_volume = get_column_volume_xlsx(df, data_dict)

        if column_volume == None or sample_flow == None:
            retention_time = None
        else:
            retention_time = column_volume / (sample_flow/120)
        frame['resin'].append(resin)
        frame['serotype'].append(serotype)
        frame['file'].append(name)
        frame['Pure'].append(pure)
        frame['Blank'].append(blank)
        frame['Column Volume (mL)'].append(column_volume)
        frame['Elution pH'].append(elution_ph)
        frame['Wash pH'].append(wash_ph)
        frame['Equlibration pH'].append(equilibration_ph)
        frame['Elution Conductivity'].append(elution_cond)
        frame['Wash Conductivity'].append(wash_cond)
        frame['Equilibration Conductivity'].append(equilibration_cond)
        frame['Sample Volume (mL)'].append(sample_volume)
        frame['System Flowrate Elution (CV/h)'].append(system_flow)
        frame['Sample Flowrate Elution (CV/h)'].append(sample_flow)
        frame['ChromID'].append(chrom_id)
        frame['Sample flowrate (CV/h)'].append(sample_flow)
        frame['Retention Time (min)'].append(retention_time)
    except Exception as e:
        print(e, csv)

data = pd.DataFrame(frame)

data.to_csv(f'outputs/collation_10_07_24/all_btec_gene_affinity_data.csv', index=False)
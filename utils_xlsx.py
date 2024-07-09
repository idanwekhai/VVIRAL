import os
import re

import numpy as np
import matplotlib.pyplot as plt


def make_dir_if_not_exists(folder):
    """
    This function takes in a folder name and creates a folder if it does not exist.
    Args:
        folder: folder name
    Returns:
        None"
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

def get_col_name_from_index(data, index):
    """
    This function takes in a dataframe and an index and returns the column name.
    Args:
        data: dataframe
        index: index of the column
    Returns:
        column name"""
    return data.columns[index]

def load_useful_data(data):
    """
    This function takes in a dataframe and returns a dictionary with useful data.
    Args:
        data: dataframe
    Returns:
        data_dict: dictionary with useful data
    """
    pH = list(data.columns).index('pH')

    uv_280 = list(data.columns).index('mAU')
    uv_260 = list(data.columns).index('mAU.1')
    conductivity = list(data.columns).index('mS/cm')
    sample_flow = list(data.columns).index('CV/h')
    system_flow = list(data.columns).index('CV/h.1')
    sample_pressure = list(data.columns).index('MPa')
    system_pressure = list(data.columns).index('MPa.1')
    # run_log = list(data.columns).index('Logbook')
    run_log = list(data.columns).index('Fraction.2')
    injection = list(data.columns).index('Fraction.1')

    ml_pH = pH - 1
    ml_uv_280 = uv_280 - 1
    ml_uv_260 = uv_260 - 1
    ml_conductivity = conductivity - 1
    ml_sample_flow = sample_flow - 1
    ml_system_flow = system_flow - 1
    ml_sample_pressure = sample_pressure - 1
    ml_system_pressure = system_pressure - 1
    ml_run_log = run_log - 1
    ml_injection = injection - 1

    data_dict = {'pH': [get_col_name_from_index(data, ml_pH), get_col_name_from_index(data, pH)],
                'UV_280': [get_col_name_from_index(data, ml_uv_280), get_col_name_from_index(data, uv_280)], 
                'UV_260': [get_col_name_from_index(data, ml_uv_260), get_col_name_from_index(data, uv_260)], 
                'Conductivity': [get_col_name_from_index(data, ml_conductivity), get_col_name_from_index(data, conductivity)], 
                'Sample Flow': [get_col_name_from_index(data, ml_sample_flow), get_col_name_from_index(data, sample_flow)], 
                'System Flow': [get_col_name_from_index(data, ml_system_flow), get_col_name_from_index(data, system_flow)], 
                'Sample Pressure': [get_col_name_from_index(data, ml_sample_pressure), get_col_name_from_index(data, sample_pressure)], 
                'System Pressure': [get_col_name_from_index(data, ml_system_pressure), get_col_name_from_index(data, system_pressure)],
                'Run Log': [get_col_name_from_index(data, ml_run_log), get_col_name_from_index(data, run_log)],
                'Injection': [get_col_name_from_index(data, ml_injection), get_col_name_from_index(data, injection)]}
    return data_dict

def get_chrom_id(df, data_dict):
    """
    This function takes in a dataframe and a dictionary with useful data and returns the chromatography id.
    Args:
        df: dataframe
        data_dict: dictionary with useful data
    Returns:
        chrom_id: chromatography id
    """
    ml_injection = data_dict['Injection'][0]
    injection = data_dict["Injection"][1]
    vals = df[injection].values
    if 'ChromID' in vals:
        # chrom_id = df[ml_injection].values[-1]
        idx = df.index[df[injection] == 'ChromID']
        chrom_id = df[ml_injection].loc[idx].values[0]
    else:
        chrom_id = None
    return chrom_id

def get_column_volume(df, data_dict):
    """
    This function takes in a dataframe and a dictionary with useful data and returns the column volume.
    Args:
        df: dataframe
        data_dict: dictionary with useful data
    Returns:
        column_volume: columne_volume
    """
    ml_injection = data_dict['Injection'][0]
    injection = data_dict["Injection"][1]
    vals = df[injection].values
    if 'ColumnVolume (ml)' in vals:
        idx = df.index[df[injection] == 'ColumnVolume (ml)']
        column_volume = df[ml_injection].loc[idx].values[0]
    else:
        column_volume = None
    return column_volume

def get_resin(name):
    """
    This function takes in a name and returns the resin used.
    Args:
        name: name of the file
    Returns:
        resin: resin used
    """
    resin = re.findall(r'AAV[A-Z]\d+', name)
    if len(resin) == 0:
        resin = re.findall(r'AAV[xX]', name)
        if len(resin) == 0:
            resin = re.findall(r'[aA]10', name)
            if len(resin) == 0:
                resin = 'Unknown'
    return resin[0]

def get_serotype(name):
    """
    This function takes in a name and returns the serotype of AAV.
    Args:
        name: name of the file
    Returns:
        serotype: serotype of AAV
    """
    serotype = re.findall(r'AAV*\d+', name)
    if len(serotype) == 0:
        serotype = 'Unknown'
    return serotype[0]

def get_resin_and_serotype(name):
    """
    This function takes in a name and returns the resin used and serotype of AAV.
    Args:
        name: name of the file
    Returns:
        resin: resin used
        serotype: serotype of AAV
    """
    resin = get_resin(name)
    serotype = get_serotype(name)

    return resin, serotype

def get_column_volume(name):
    """
    This function takes in a name and returns the column volume.
    Args:
        name: name of the file
    Returns:    
        column_volume: column volume
    """
    column_volume = re.findall(r'\d+(?:\.\d+)?[mM][lL]', name)
    if len(column_volume) == 0:
        column_volume = 'Unknown'
    return column_volume[0]

def is_pure(name):
    """
    This function takes in a name and returns if the sample is pure or not.
    Args:
        name: name of the file
    Returns:
        pure: True if the sample is pure, False otherwise
    """
    pure = re.findall(r'[pP]ure', name)
    if len(pure) == 0:
        pure = False
    else:
        pure = True
    return pure

def is_blank(name):
    """
    This function takes in a name and returns if the run is blank or not.
    Args:
        name: name of the file
    Returns:
        pure: True if the run is blank, False otherwise
    """
    blank = re.findall(r'[bB]lank', name)
    if len(blank) == 0:
        blank = False
    else:
        blank = True
    return blank 


def plot_data(data, folder, name, data_dict, columns=['UV_280', 'Conductivity']):
    """
    This function takes in a dataframe and plots the data.
    Args:
        data: dataframe
        folder: folder to save the plots
        name: name of the plot
        data_dict: dictionary with useful data
        columns: list of columns to plot
    Returns:
        None"""
    plt.rcParams["figure.figsize"] = (20,10)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(data[data_dict[columns[0]][0]], data[data_dict[columns[0]][1]], 'g-', label=columns[0])
    ax2.plot(data[data_dict[columns[0]][0]], data[data_dict[columns[1]][1]], 'b-', label=columns[1]) 
    ax1.set_xlabel('Volume (ml)')
    ax1.set_ylabel('mAU', color='g')
    ax2.set_ylabel('mS/cm', color='b')
    resin, serotype = get_resin_and_serotype(name)
    plt.title(f'Resin: {resin}, Serotype: {serotype}')
    plt.legend()
    fig.savefig(f'{folder}/plots/{name}.png')
    fig.clf()
    fig.clear()

def get_useful_log_idx(data):
    log_name = []
    useful_log_idx = []
    for i in range(len(data)):
        if type(data['Fraction.2'].values[i]) == str:
            if data['Fraction.2'].values[i][:5] == "Phase":
                j = data['Fraction.2'].values[i]
                log_name.append(re.search(r'Phase (.*?) \(Issued\)', j).group(1))
                useful_log_idx.append(i)
    return log_name, useful_log_idx
    
def get_ph_and_cond_at_elution(df, data_dict):
    """
    This function takes in a dataframe and a dictionary with useful data and returns the pH and conductivity at elution.
    Args:
        df: dataframe
        data_dict: dictionary with useful data
    Returns:
        elution_ph: pH at elution
        elution_cond: conductivity at elution
    """
    ml_pH_col = data_dict['pH'][0]
    ml_cond_col = data_dict['Conductivity'][0]
    ml_log_col = data_dict['Run Log'][0]

    run_log, useful_log_idx = get_useful_log_idx(df)

    if 'Elution' in run_log:
        elution_idx = useful_log_idx[run_log.index('Elution')]
        elution_ml = df[ml_log_col][elution_idx]
        elution_ph_idx = np.searchsorted(df[ml_pH_col], elution_ml, side="left")
        elution_cond_idx = np.searchsorted(df[ml_cond_col], elution_ml, side="left")
        elution_ph = round(df['pH'][elution_ph_idx], 2)
        elution_cond = round(df['mS/cm'][elution_cond_idx], 2)
    elif 'Elution 1' in run_log:
        elution_idx = useful_log_idx[run_log.index('Elution 1')]
        elution_ml = df[ml_log_col][elution_idx]
        elution_ph_idx = np.searchsorted(ml_pH_col, elution_ml, side="left")
        elution_cond_idx = np.searchsorted(ml_cond_col, elution_ml, side="left")
        elution_ph = round(df['pH'][elution_ph_idx], 2)
        elution_cond = round(df['mS/cm'][elution_cond_idx], 2)
    else:
        elution_ph = None
        elution_cond = None
    return elution_ph, elution_cond

def get_ph_and_cond_at_wash(df, data_dict):
    """
    This function takes in a dataframe and a dictionary with useful data and returns the pH and conductivity at wash.
    Args:
        df: dataframe
        data_dict: dictionary with useful data
    Returns:
        wash_ph: pH at wash
        wash_cond: conductivity at wash
    """
    ml_pH_col = data_dict['pH'][0]
    ml_cond_col = data_dict['Conductivity'][0]
    ml_log_col = data_dict['Run Log'][0]

    run_log, useful_log_idx = get_useful_log_idx(df)

    # print('wash')
    if 'Column Wash' in run_log:
        column_wash_idx = useful_log_idx[run_log.index('Column Wash')]
        column_wash_ml = df[ml_log_col][column_wash_idx]
        wash_ph_index = np.searchsorted(df[ml_pH_col], column_wash_ml, side="left")
        wash_cond_index = np.searchsorted(df[ml_cond_col], column_wash_ml, side="left")
        wash_ph = round(df['pH'][wash_ph_index], 2)
        wash_cond = round(df['mS/cm'][wash_cond_index], 2)
    elif 'Column Wash 1' in run_log:
        column_wash_idx = useful_log_idx[run_log.index('Column Wash 1')]
        column_wash_ml = df[ml_log_col][column_wash_idx]
        wash_ph_index = np.searchsorted(df[ml_pH_col], column_wash_ml, side="left")
        wash_cond_index = np.searchsorted(df[ml_cond_col], column_wash_ml, side="left")
        wash_ph = round(df['pH'][wash_ph_index], 2)
        wash_cond = round(df['mS/cm'][wash_cond_index], 2)
    else:
        wash_ph = None
        wash_cond = None
    return wash_ph, wash_cond

def get_ph_and_cond_at_equilibration(df, data_dict):
    """
    This function takes in a dataframe and a dictionary with useful data and returns the pH and conductivity at equilibration.
    Args:
        df: dataframe
        data_dict: dictionary with useful data
    Returns:
        equilibration_ph: pH at equilibration
        equilibration_cond: conductivity at equilibration
    """
    ml_pH_col = data_dict['pH'][0]
    ml_cond_col = data_dict['Conductivity'][0]
    ml_log_col = data_dict['Run Log'][0]

    run_log, useful_log_idx = get_useful_log_idx(df)

    if 'Equilibration' in run_log:
        column_equilibration_idx = useful_log_idx[run_log.index('Equilibration')]
        column_equilibration_ml = df[ml_log_col][column_equilibration_idx]
        equilibration_ph_index = np.searchsorted(df[ml_pH_col], column_equilibration_ml, side="left")
        equilibration_cond_index = np.searchsorted(df[ml_cond_col], column_equilibration_ml, side="left")
        equilibration_ph = round(df['pH'][equilibration_ph_index], 2)
        equilibration_cond = round(df['mS/cm'][equilibration_cond_index], 2)
    else:
        equilibration_ph = None
        equilibration_cond = None

    return equilibration_ph, equilibration_cond

def get_sample_and_sytem_flow_rate_at_wash(df, data_dict):
    """
    This function takes in a dataframe and a dictionary with useful data and returns the sample and system flow rate at wash.
    Args:
        df: dataframe
        data_dict: dictionary with useful data
    Returns:
        sample_flow: sample flow rate at wash
        system_flow: system flow rate at wash
    """
    ml_sample_flow_col = data_dict['Sample Flow'][0]
    ml_system_flow_col = data_dict['System Flow'][0]
    ml_log_col = data_dict['Run Log'][0]
    
    run_log, useful_log_idx = get_useful_log_idx(df)

    if 'Column Wash' in run_log:
        column_wash_idx = useful_log_idx[run_log.index('Column Wash')]
    elif 'Column Wash 1' in run_log:
        column_wash_idx = useful_log_idx[run_log.index('Column Wash 1')]
    else:
        column_wash_idx = None


    if column_wash_idx is not None:
        column_wash_ml = df[ml_log_col][column_wash_idx]
        sample_wash_index = np.searchsorted(df[ml_sample_flow_col], column_wash_ml, side="left")
        system_wash_index = np.searchsorted(df[ml_system_flow_col], column_wash_ml, side="left")
        sample_flow = round(df[ml_sample_flow_col][sample_wash_index], 2)
        system_flow = round(df[ml_system_flow_col][system_wash_index ], 2)
    else:
        sample_flow = None
        system_flow = None
    return sample_flow, system_flow

def get_sample_and_sytem_flow_rate_at_elution(df, data_dict):
    """
    This function takes in a dataframe and a dictionary with useful data and returns the sample and system flow rate at elution.
    Args:
        df: dataframe
        data_dict: dictionary with useful data
    Returns:
        sample_flow: sample flow rate at elution
        system_flow: system flow rate at elution
    """
    ml_sample_flow_col = data_dict['Sample Flow'][0]
    ml_system_flow_col = data_dict['System Flow'][0]
    ml_log_col = data_dict['Run Log'][0]

    run_log, useful_log_idx = get_useful_log_idx(df)

    if 'Elution' in run_log:
        elution_idx = useful_log_idx[run_log.index('Elution')]
        elution_ml = df[ml_log_col][elution_idx]
        system_elution_index = np.searchsorted(df[ml_system_flow_col], elution_ml, side="left")
        sample_elution_index = np.searchsorted(df[ml_sample_flow_col], elution_ml, side="left")
        sample_flow = round(df[ml_sample_flow_col][sample_elution_index], 2)
        system_flow = round(df[ml_system_flow_col][system_elution_index ], 2)
    elif 'Elution 1' in run_log:
        elution_idx = useful_log_idx[run_log.index('Elution 1')]
        elution_ml = df[ml_log_col][elution_idx]
        system_elution_index = np.searchsorted(df[ml_system_flow_col], elution_ml, side="left")
        sample_elution_index = np.searchsorted(df[ml_sample_flow_col], elution_ml, side="left")
        sample_flow = round(df[ml_sample_flow_col][sample_elution_index], 2)
        system_flow = round(df[ml_system_flow_col][system_elution_index ], 2)
    else:
        sample_flow = None
        system_flow = None
    return sample_flow, system_flow

def get_sample_and_sytem_flow_rate_at_equilibration(df, data_dict):
    """
    This function takes in a dataframe and a dictionary with useful data and returns the sample and system flow rate at equilibration.
    Args:
        df: dataframe
        data_dict: dictionary with useful data
    Returns:
        sample_flow: sample flow rate at equilibration
        system_flow: system flow rate at equilibration
    """
    ml_sample_flow_col = data_dict['Sample Flow'][0]
    ml_system_flow_col = data_dict['System Flow'][0]
    ml_log_col = data_dict['Run Log'][0]

    run_log, useful_log_idx = get_useful_log_idx(df)

    if 'Equilibration' in run_log:
        equilibration_idx = useful_log_idx[run_log.index('Equilibration')]
        equilibration_ml = df[ml_log_col][equilibration_idx]
        system_equilibration_index = np.searchsorted(df[ml_system_flow_col], equilibration_ml, side="left")
        sample_equilibration_index = np.searchsorted(df[ml_sample_flow_col], equilibration_ml, side="left")
        sample_flow = round(df[ml_sample_flow_col][sample_equilibration_index], 2)
        system_flow = round(df[ml_system_flow_col][system_equilibration_index], 2)
    else:
        sample_flow = None
        system_flow = None
    return sample_flow, system_flow

def get_sample_volume(df, data_dict):
    """
    This function takes in a dataframe and a dictionary with useful data and returns the sample volume.
    Args:
        df: dataframe
        data_dict: dictionary with useful data
    Returns:
        sample_volume: sample volume
    """
    ml_log_col = data_dict['Run Log'][0]

    run_log, useful_log_idx = get_useful_log_idx(df)

    if 'Column Wash' in run_log:
        column_wash_idx = useful_log_idx[run_log.index('Column Wash')]
    elif 'Column Wash 1' in run_log:
        column_wash_idx = useful_log_idx[run_log.index('Column Wash 1')]
    else:   
        column_wash_idx = None

    if 'Sample Application' in run_log:
        sample_application_idx = useful_log_idx[run_log.index('Sample Application')]
    else:
        sample_application_idx = None
    
    if column_wash_idx is not None and sample_application_idx is not None:
        sample_volume = df[ml_log_col][column_wash_idx] - df[ml_log_col][sample_application_idx]
    else:
        sample_volume = None
    return sample_volume


def get_start_stop_idx(dataframe):
    two_elutions = False
    try:
        log_vals = dataframe['Logbook'].values
    
        if 'Elution' in log_vals:
            elution_idx = dataframe.index[dataframe['Logbook'] == 'Elution'].tolist()[-1]
        elif 'Elution 1' in log_vals:
            elution_idx = dataframe.index[dataframe['Logbook'] == 'Elution 1'].tolist()[-1]
            two_elutions = True
        else:
            elution_idx = None
        
        if 'Column Wash' in dataframe['Logbook'].values:
            column_wash_idx = dataframe.index[dataframe['Logbook'] == 'Column Wash'].tolist()[-1]
        elif 'Column Wash 1' in dataframe['Logbook'].values:
            column_wash_idx = dataframe.index[dataframe['Logbook'] == 'Column Wash 2'].tolist()[-1]
        else:
            column_wash_idx = None

        if 'Column CIP' in dataframe['Logbook'].values:
            stop_idx = dataframe.index[dataframe['Logbook'] == 'Column CIP'].tolist()[-1]
        else:
            stop_idx = None
    except:
        start_idx = None
        stop_idx = None
        
    if elution_idx != None:
        start_idx = elution_idx
    else:
        start_idx = column_wash_idx
    return start_idx, stop_idx, two_elutions


def query_line(volume, results):
    row_0 = [i for i in results[0]]
    row_1 = [volume[round(i)] for i in results[1]]
    row_2 = [volume[round(i)] for i in results[2]]
    return [row_0, row_1, row_2]

def show_peaks(name, uv_280, volume, peaks, half_width, contour_heights):
    plt.rcParams["figure.figsize"] = (20,10)
    plt.plot(volume, uv_280)
    plt.plot(volume[peaks], uv_280[peaks], "x")
    plt.hlines(y=0, xmin=min(volume), xmax=max(volume), linestyle="dashed", color="gray" )
    plt.hlines(*half_width, color="C2")
    plt.vlines(x=volume[peaks], ymin=contour_heights, ymax=uv_280[peaks])
    plt.savefig(f'inspect_plots/{name}.png')
    plt.clf()
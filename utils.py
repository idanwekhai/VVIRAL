import os
import re
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
    run_log = list(data.columns).index('Logbook')

    ml_pH = pH - 1
    ml_uv_280 = uv_280 - 1
    ml_uv_260 = uv_260 - 1
    ml_conductivity = conductivity - 1
    ml_sample_flow = sample_flow - 1
    ml_system_flow = system_flow - 1
    ml_sample_pressure = sample_pressure - 1
    ml_system_pressure = system_pressure - 1
    ml_run_log = run_log - 1

    data_dict = {'pH': [get_col_name_from_index(data, ml_pH), get_col_name_from_index(data, pH)],
                'UV_280': [get_col_name_from_index(data, ml_uv_280), get_col_name_from_index(data, uv_280)], 
                'UV_260': [get_col_name_from_index(data, ml_uv_260), get_col_name_from_index(data, uv_260)], 
                'Conductivity': [get_col_name_from_index(data, ml_conductivity), get_col_name_from_index(data, conductivity)], 
                'Sample Flow': [get_col_name_from_index(data, ml_sample_flow), get_col_name_from_index(data, sample_flow)], 
                'System Flow': [get_col_name_from_index(data, ml_system_flow), get_col_name_from_index(data, system_flow)], 
                'Sample Pressure': [get_col_name_from_index(data, ml_sample_pressure), get_col_name_from_index(data, sample_pressure)], 
                'System Pressure': [get_col_name_from_index(data, ml_system_pressure), get_col_name_from_index(data, system_pressure)],
                'Run Log': [get_col_name_from_index(data, ml_run_log), get_col_name_from_index(data, run_log)]}
    return data_dict

def get_resin_and_serotype(name):
    """
    This function takes in a name and returns the resin used and serotype of AAV.
    Args:
        name: name of the file
    Returns:
        resin: resin used
        serotype: serotype of AAV
    """
    resin = re.findall(r'AAV[A-Z]\d+', name)
    serotype = re.findall(r'AAV*\d+', name)
    if len(resin) == 0:
        resin = 'Unknown'
    if len(serotype) == 0:
        serotype = 'Unknown'
    return resin[0], serotype[0]

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
        resin = re.findall(r'AAVX', name)
        if len(resin) == 0:
            resin = re.findall(r'AAVx', name)
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
    log_col = data_dict['Run Log'][1]
    ml_log_col = data_dict['Run Log'][0]

    # print('elu')
    elution_ph_index = df[ml_pH_col][round(df[ml_pH_col]) == round(df[ml_log_col][4])].index[1]
    elution_cond_index = df[ml_cond_col][round(df[ml_cond_col]) == round(df[ml_log_col][4])].index[1]
    elution_ph = round(df['pH'][elution_ph_index], 2)
    elution_cond = round(df['mS/cm'][elution_cond_index], 2)

    if 'Elution' in df[log_col].values:
        elution_idx = df.index[df[log_col] == 'Elution'].tolist()[-1]
        wash_ph_index = df[ml_pH_col][round(df[ml_pH_col]) == round(df[ml_log_col][elution_idx])].index[1]
        wash_cond_index = df[ml_cond_col][round(df[ml_cond_col]) == round(df[ml_log_col][elution_idx])].index[1]
        elution_ph = round(df['pH'][wash_ph_index], 2)
        elution_cond = round(df['mS/cm'][wash_cond_index], 2)
    elif 'Elution 1' in df[log_col].values:
        elution_idx = df.index[df[log_col] == 'Elution 1'].tolist()[-1]
        wash_ph_index = df[ml_pH_col][round(df[ml_pH_col]) == round(df[ml_log_col][elution_idx])].index[1]
        wash_cond_index = df[ml_cond_col][round(df[ml_cond_col]) == round(df[ml_log_col][elution_idx])].index[1]
        elution_ph = round(df['pH'][wash_ph_index], 2)
        elution_cond = round(df['mS/cm'][wash_cond_index], 2)
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
    log_col = data_dict['Run Log'][1]
    ml_log_col = data_dict['Run Log'][0]

    # print('wash')
    if 'Column Wash' in df[log_col].values:
        column_wash_idx = df.index[df[log_col] == 'Column Wash'].tolist()[-1]
        wash_ph_index = df[ml_pH_col][round(df[ml_pH_col]) == round(df[ml_log_col][column_wash_idx])].index[1]
        wash_cond_index = df[ml_cond_col][round(df[ml_cond_col]) == round(df[ml_log_col][column_wash_idx])].index[1]
        wash_ph = round(df['pH'][wash_ph_index], 2)
        wash_cond = round(df['mS/cm'][wash_cond_index], 2)
    elif 'Column Wash 1' in df[log_col].values:
        column_wash_idx = df.index[df['Logbook'] == 'Column Wash 1'].tolist()[-1]
        wash_ph_index = df[ml_pH_col][round(df[ml_pH_col]) == round(df[ml_log_col][column_wash_idx])].index[1]
        wash_cond_index = df[ml_cond_col][round(df[ml_cond_col]) == round(df[ml_log_col][column_wash_idx])].index[1]
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
    log_col = data_dict['Run Log'][1]
    ml_log_col = data_dict['Run Log'][0]

    if 'Equilibration' in df[log_col].values:
        column_equilibration_idx = df.index[df[log_col] == 'Equilibration'].tolist()[-1]
        equilibration_ph_index = df[ml_pH_col][round(df[ml_pH_col]) == round(df[ml_log_col][column_equilibration_idx])].index[1]
        equilibration_cond_index = df[ml_cond_col][round(df[ml_cond_col]) == round(df[ml_log_col][column_equilibration_idx])].index[1]
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
    log_col = data_dict['Run Log'][1]

    if 'Column Wash' in df[log_col].values:
        column_wash_idx = df.index[df[log_col] == 'Column Wash'].tolist()[-1]
    elif 'Column Wash 1' in df[log_col].values:
        column_wash_idx = df.index[df[log_col] == 'Column Wash 1'].tolist()[-1]
    else:
        column_wash_idx = None

    if column_wash_idx is not None:
        system_wash_index = df[ml_system_flow_col][round(df[ml_system_flow_col]) == round(df[ml_log_col][column_wash_idx])].index[1]
        sample_wash_index = df[ml_sample_flow_col][round(df[ml_sample_flow_col]) == round(df[ml_log_col][column_wash_idx])].index[1]
        sample_flow = round(df[ml_sample_flow_col][system_wash_index], 2)
        system_flow = round(df[ml_system_flow_col][sample_wash_index ], 2)
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
    log_col = data_dict['Run Log'][1]

    if 'Elution' in df[log_col].values:
        elution_idx = df.index[df[log_col] == 'Elution'].tolist()[-1]
        system_elution_index = df[ml_system_flow_col][round(df[ml_system_flow_col]) == round(df[ml_log_col][elution_idx])].index[1]
        sample_elution_index = df[ml_sample_flow_col][round(df[ml_sample_flow_col]) == round(df[ml_log_col][elution_idx])].index[1]
        sample_flow = round(df[ml_sample_flow_col][system_elution_index], 2)
        system_flow = round(df[ml_system_flow_col][sample_elution_index ], 2)
    elif 'Elution 1' in df[log_col].values:
        elution_idx = df.index[df[log_col] == 'Elution 1'].tolist()[-1]
        system_elution_index = df[ml_system_flow_col][round(df[ml_system_flow_col]) == round(df[ml_log_col][elution_idx])].index[1]
        sample_elution_index = df[ml_sample_flow_col][round(df[ml_sample_flow_col]) == round(df[ml_log_col][elution_idx])].index[1]
        sample_flow = round(df[ml_sample_flow_col][system_elution_index], 2)
        system_flow = round(df[ml_system_flow_col][sample_elution_index ], 2)
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
    log_col = data_dict['Run Log'][1]

    if 'Equilibration' in df[log_col].values:
        equilibration_idx = df.index[df[log_col] == 'Equilibration'].tolist()[-1]
        system_equilibration_index = df[ml_system_flow_col][round(df[ml_system_flow_col]) == round(df[ml_log_col][equilibration_idx])].index[1]
        sample_equilibration_index = df[ml_sample_flow_col][round(df[ml_sample_flow_col]) == round(df[ml_log_col][equilibration_idx])].index[1]
        sample_flow = round(df[ml_sample_flow_col][system_equilibration_index], 2)
        system_flow = round(df[ml_system_flow_col][sample_equilibration_index ], 2)
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
    log_col = data_dict['Run Log'][1]

    if 'Column Wash' in df[log_col].values:
        column_wash_idx = df.index[df[log_col] == 'Column Wash'].tolist()[-1]
    elif 'Column Wash 1' in df[log_col].values:
        column_wash_idx = df.index[df[log_col] == 'Column Wash 1'].tolist()[-1]
    else:   
        column_wash_idx = None

    if 'Sample Application' in df[log_col].values:
        sample_application_idx = df.index[df[log_col] == 'Sample Application'].tolist()[-1]
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
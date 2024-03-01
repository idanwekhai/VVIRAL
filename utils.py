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
                'System_flow': [get_col_name_from_index(data, ml_system_flow), get_col_name_from_index(data, system_flow)], 
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
    ml_log_col = data_dict['Run Log'][0]
    # print('elu')
    elution_ph_index = df[ml_pH_col][round(df[ml_pH_col]) == round(df[ml_log_col][4])].index[1]
    elution_cond_index = df[ml_cond_col][round(df[ml_cond_col]) == round(df[ml_log_col][4])].index[1]
    elution_ph = round(df['pH'][elution_ph_index], 2)
    elution_cond = round(df['mS/cm'][elution_cond_index], 2)
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
    # print('wash')
    wash_ph_index = df[ml_pH_col][round(df[ml_pH_col ]) == round(df[ml_log_col][3])].index[1]
    wash_cond_index = df[ml_cond_col][round(df[ml_cond_col]) == round(df[ml_log_col][3])].index[1]
    wash_ph = round(df['pH'][wash_ph_index], 2)
    wash_cond = round(df['mS/cm'][wash_cond_index], 2)
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
    # print('eqil')
    equilibration_ph_index = df[ml_pH_col][round(df[ml_pH_col ]) == round(df[ml_log_col][1])].index[1]
    equilibration_cond_index = df[ml_cond_col][round(df[ml_cond_col]) == round(df[ml_log_col][1])].index[1]
    equilibration_ph = round(df['pH'][equilibration_ph_index], 2)
    equilibration_cond = round(df['pH'][equilibration_cond_index], 2)
    return equilibration_ph, equilibration_cond

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
    sample_volume = df[ml_log_col][4] - df[ml_log_col][3]
    return sample_volume
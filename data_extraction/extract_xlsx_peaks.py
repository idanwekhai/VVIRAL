import os
from zipfile import ZipFile
import pandas as pd
import xmltodict

folder = '/home/kelidan/VVIRAL/data_dump/BTEC_Ufol/Gene Therapy Results'
ZIPS = []
for root, dirs, files in os.walk(f"{folder}"):
    for file in files:
        if file.endswith(".Result"):
            ZIPS.append(os.path.join(root, file))
print(len(ZIPS))


def zip2dict(inp):
    """
    input = zip object
    outout = dict with filename:file-object pairs
    """
    mydict = {}
    for i in inp.NameToInfo:
        tmp_dict = {i: inp.read(i)}
        mydict.update(tmp_dict)
    return mydict

col_names = ['StartPeakLimitType', 'EndPeakLimitType', 'Name', 'Width', 'Area', 'Height', 
             'StartPeakRetention', 'MaxPeakRetention', 'EndPeakRetention', 'WidthAtHalfHeight',
             'PercentOfTotalArea', 'PercentOfTotalPeakArea', 'StartPeakEndpointHeight', 
             'EndPeakEndpointHeight', 'StartBaseLineHeight', 'MaxBaseLineHeight', 'EndBaseLineHeight', 
             'StartPeakVial', 'MaxPeakVial', 'EndPeakVial', 'Sigma', 'Assymetry', 'AssymetryPeakStart', 
             'AssymetryPeakEnd', 'StartConductivityHeight', 'MaxConductivityHeight', 'EndConductivityHeight', 
             'AverageConductivity', 'IsStandardPeak', 'file']

df_data = [[], [], []]


for i in ZIPS:
    try:
        with open(i, 'rb') as f:
            input_zip = ZipFile(f)
            zip_data = zip2dict(input_zip)
            xml_read = xmltodict.parse(zip_data['Chrom.1.Xml'])
    except:
        xml_read = None

    try:
        data = xml_read['Chromatogram']['PeakTables']['PeakTable']['Peaks']['Peak']
    except:
        data = None

    try:
        events = xml_read['Chromatogram']['EventCurves']['EventCurve'][2]['Events']['Event']
        
        for event in range(len(events)):
            if "Phase Elution" in events[event]['EventText']:
                elution_start = float(events[event]['EventVolume'])
                col_volume = float(xml_read['Chromatogram']['EventCurves']['EventCurve'][2]['ColumnVolume'])
    except:
        elution_start = None
        col_volume = None

    if data:
        peaks = xml_read['Chromatogram']['PeakTables']['PeakTable']['Peaks']['Peak']
        if type(peaks) != list:
            peaks = [peaks]
        if len(peaks) <= 3:
            for j in range(len(peaks)):
                if len(peaks) != 0:
                    peaks[j]['file'] = i.split('/')[-1][:-7]
                    peaks[j]['ChromID'] = xml_read['Chromatogram']['ChromatogramID']
                    peaks[j]['elution_start'] = elution_start
                    peaks[j]['Column Volume (mL)'] = col_volume
                    df_data[j].append(peaks[j])
    
        
df1 = pd.DataFrame(df_data[0])
df2 = pd.DataFrame(df_data[1])
df3 = pd.DataFrame(df_data[2])

df1.to_csv('outputs/peak_data1.csv', index=False)
df2.to_csv('outputs/peak_data2.csv', index=False)
df3.to_csv('outputs/peak_data3.csv', index=False)
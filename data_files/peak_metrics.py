import math
import numpy as np

def tailing_factor(peaks, results):
    res = []
    for i in range(len(peaks)):
        a = peaks[i] - results[1][i]
        b = results[2][i] - peaks[i]
        Tf = (a+b) / (2*a)
        res.append(Tf)
    return res

def peak_assymetry(peaks, results):
    res = []
    for i in range(len(peaks)):
        a = peaks[i] - results[1][i]
        b = results[2][i] - peaks[i]
        res.append(b/a)
    return res

def number_of_theoretical_plates(volume, peaks, results):
    res = []
    for i in range(len(peaks)):
        retention_volume = volume[peaks[i]]
        #width = results[i]
        width = volume[round(results[2][i])] - volume[round(results[1][i])]
        N = 5.54 * (retention_volume/width)**2
        res.append(N)
    return res

def area(volume, peaks, results, height):
    res = []
    n_plates = number_of_theoretical_plates(volume, peaks, results)
    for i in range(len(peaks)):
        retention_volume = volume[peaks[i]]
        H = height[i]
        N = n_plates[i]
        denominator = math.sqrt(N / (2*math.pi))
        # print(data['ml'][peaks[i]])
        area = (retention_volume * H) / denominator
        res.append(area)
    return res

def peak_height(peaks, height):
    """
    Returns the height of the peaks
    Args:
    peaks: list of integers
    height: list of floats
    
    Returns:
    res: list of floats
    """
    res = []
    for i in range(len(peaks)):
        res.append(height[i])
    return res

def integrate_peak(peaks, info, data):
    """
    Returns the integrated area of the peaks
    Args:
    peaks: list of integers
    info: list of floats
    
    Returns:
    res: list of floats
    """
    res = []
    for i in range(len(peaks)):
        lower = info['left_bases'][i]
        upper = info['right_bases'][i]
        integrated_area = np.trapz(data[lower:upper])
        res.append(integrated_area)
    return res

def integrate_peak_2(peaks, info, data):
    """
    Returns the integrated area of the peaks
    Args:
    peaks: list of integers
    info: list of floats
    
    Returns:
    res: list of floats
    """
    res = []
    for i in range(len(peaks)):
        lower = info['left_bases'][i]
        upper = info['right_bases'][i]
        integrated_area = np.trapezoid(data[lower:upper])
        res.append(integrated_area)
    return res
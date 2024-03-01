import math

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
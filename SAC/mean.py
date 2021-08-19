
# Standard python numerical analysis imports:
import numpy as np
from scipy import signal
import scipy.interpolate #import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
from scipy.signal import find_peaks, peak_prominences
#import pandas as pd
#import peakutils

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
#import h5py

import sys

#from scipy.interpolate import spline


""" def sac_dm(data, N):
	M = len(data)
	
	size = int(M/N)
	sacdm=[0.0] * size

	start = 0
	end = N
	for k in range(size):
		peaks, _ = find_peaks(data[start:end])
		v = np.array(peaks)
		sacdm[k] = 1.0*len(v)/N
		start = end
		end += N

	return sacdm """

def sac_dm(data, N):
	M = len(data)
	
	size = int(M/N)
	sacdm=[0.0] * size

	start = 0
	end = N
	for k in range(size):
		peaks, _ = find_peaks(data[start:end])
		v = np.array(peaks)
		sacdm[k] = (1.0*len(v)/N)
		start = end
		end += N

	return sacdm

def sac_am(data, N):
    M = len(data)
    
    size = int(M/N)
    sacam = [0.0] * size

    start = 0
    end = N

    for k in range(size):
    
        peaks, _ = find_peaks(data[start:end])
        v = []
        for p in range(len(data[peaks])): v.append(data[peaks][p][0]) 
        s = sum(np.absolute(v))
        sacam[k] = 1.0*s/N
        start = end
        end += N

    return sacam

	


#********* Main ********



N = int(sys.argv[3])
file1 = sys.argv[1]
file2 = sys.argv[2]

#data1 = np.genfromtxt(file, delimiter=',', names=['t', 'x', 'y','z'])
#data2 = np.genfromtxt(file2, delimiter=',', names=['t', 'x', 'y','z'])
data1 = np.genfromtxt(file1, delimiter='\n', names=['z'])
data2 = np.genfromtxt(file2, delimiter='\n', names=['z'])

sac = sac_dm(data1, N)
sac2 = sac_dm(data2, N)

fig = plt.figure()


ax = fig.add_subplot(211)
ax.set_title("Comparando Sinal Normal com Sinal Com Falha usando SAC-AM")   
ax.plot(data1,color='b', label='Signal 1')
ax.plot(data2,color='r', label='Signal 2')
plt.ylabel('Amplitude') 
#plt.xlabel('Time (sec.)')
ax.legend(['Sinal Normal', 'Sinal com Falhas'], loc='upper right')

x = np.array(range(0, len(sac)))
x = x * N

x2 = np.array(range(0, len(sac2)))
x2 = x2 * N


ax3 = fig.add_subplot(212)
ax3.plot(x, sac, color='b', label='SAC-DM 1')
ax3.plot(x2, sac2, color='r', label='SAC-DM 2')
plt.ylabel('Frequency') 
plt.xlabel('Time (sec.)')
#ax3.legend(['SAC-DM 1', 'SAC-DM 2'], loc='upper right')



""" fig2 = plt.figure()
ax2 = fig2.add_subplot(111)


kwargs = dict(histtype='stepfilled', alpha=0.3, density=True, bins=40, ec="k")

plt.hist(sac, **kwargs)
plt.hist(sac2, **kwargs) """

#plt.savefig('alignment.png', format='png')
plt.show()





	






import csv
import statistics
# Standard python numerical analysis imports:
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
from scipy.signal import find_peaks, peak_prominences
#import pandas as pd
#import peakutils

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
#import h5py
import sys

import scipy.interpolate  

def sac_dm(data, N):
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

	return sacdm

# Calcula SAC-AM utilizando a funcao find_peaks do Python
def sac_am(data, N):
    M = len(data)
    
    size = int(M/N)
    sacam = [0.0] * size

    start = 0
    end = N

    for k in range(size):
    
        peaks, _ = find_peaks(data[start:end])
        v = []
        for i in range(len(data[peaks])): v.append(data[peaks][i][0])
        s = sum(np.absolute(v))
        sacam[k] = 1.0*s/N
        start = end
        end += N

    return sacam

def plotSAC(data,imagename):
	fig3 = plt.figure()
	plt.ylabel('Frequency') 
	plt.xlabel('Time (ms)')
	ax3 = fig3.add_subplot(111)
	ax3.set_title("Signal")   
	ax3.plot(data,color='b', label='MACCD2')
	ax3.legend(['z = MACCD2'], loc='upper left')
	plt.savefig("../"+imagename+'.png')

eixo = ['x','y','z']        
N = 500

eixos = [[],[],[]]
with open('../tello-data-collect-data-stable-1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    csv_reader.__next__()
    
    for row in csv_reader:
        eixos[0].append(row[0])
        eixos[1].append(row[1])
        eixos[2].append(row[2])        

sac = sac_dm(eixos[0], 500)
sac2 = sac_dm(eixos[1], 500)
sac3 = sac_dm(eixos[2], 500)
#plotSAC(eixos[0],"sinal-tello-1")
#plotSAC(sac,"sac-tello-1")

fig = plt.figure()
fig2 = plt.figure()

ax = fig.add_subplot(311)  
ax.plot(eixos[0],color='r', label='Signal x')

ax2 = fig.add_subplot(312)
ax2.plot(eixos[1],color='g', label='Signal y')

ax3 = fig.add_subplot(313)
ax3.plot(eixos[2],color='b', label='Signal z')

ax4 = fig2.add_subplot(311)  
ax4.plot(sac,color='r', label='SAC X')

ax5 = fig2.add_subplot(312)
ax5.plot(sac2,color='g', label='SAC Y')

ax6 = fig2.add_subplot(313)
ax6.plot(sac3,color='b', label='SAC z')


plt.show()
print("Cabou!")    



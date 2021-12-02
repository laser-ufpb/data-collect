import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

from scipy.signal import find_peaks

######## READ ME ###########
#Format : testfly_data.csv 
#be sure you are in the right folder to run << data/csv/test_fly_data/data_x_y_z >>
#the testfly_data files are in folder << test_fly_data/data_x_y_z >> and can be changed with the variable "cut_or_orginal" line 33/34
#EX:d:/LASER/.venv/Scripts/python.exe analyse_data_x_y_z.py data-alexandre-grande-1.csv f1.1.1 500
#########################

def sac_dm(data, N, menorTam):
	M = menorTam
	
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

test_fly_name = sys.argv[1] # -> find name under  ..\data-collect\data_csv\test_fly_data\data_x_y_z\cut_version||orginal 
cut_or_orginal= "cut_version/"  #file directory 
#cut_or_orginal= "orginal/"  #file directory 

with open(cut_or_orginal + test_fly_name, 'rb') as f:
    clean_lines = (line.replace(b'\"',b'') for line in f)
    normal_data = np.genfromtxt(clean_lines,skip_header=1, delimiter=',',names=["x", "y", "z"])


#Figure Settings
fig, ax = plt.subplots(3,1, sharex=True, sharey=False)
fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=1.0)
fig.set_size_inches(10, 6, forward=True)
fig.suptitle(test_fly_name , fontsize=12)


ax[0].plot(normal_data['x'], color='r', label='Signal x')
ax[0].set_title('Signal x')

ax[1].plot(normal_data['y'], color='r', label='Signal y')
ax[1].set_title('Signal y')

ax[2].plot(normal_data['z'], color='r', label='Signal z')
ax[2].set_title('Signal z')


for ax in ax.flat:
    ax.set(xlabel='n-Value', ylabel='Amplitude')


print("\nFile analyse: " , f , '\n')

plt.show()




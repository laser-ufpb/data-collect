import sys
import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import find_peaks

######## READ ME ###########
#Format : testfly_data.csv
#be sure you are in the right folder to run << data/csv/test_fly_data/with_timestemp >>
#the testfly_data files are in folder << test_fly_data/with_timestemp >> and can be changed with the variable "file_directory" line 33/34
#EX: d:/LASER/.venv/Scripts/python.exe analyse_data_with_timestamp.py m5Stick_TR_drone_grande_17_09_2021_sem_vento_3.csv
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


test_fly_name = sys.argv[1] # -> find name under  ..\data-collect\data_csv\test_fly_data\with_timestamp\bad_collection||good_collection 
file_directory = "drone_grande/good_collection/"  #file directory 
#file_directory = "drone_grande/bad_collection/"  #file directory  


with open(file_directory + test_fly_name, 'rb') as f:
    normal_data = np.genfromtxt(f,skip_header=1, delimiter=',',names=['','timestamp','x', 'y','z'])


#Figure Settings
fig, ax = plt.subplots(3,1, sharex=True, sharey=False)
fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=1.0)
fig.set_size_inches(10, 6, forward=True)
fig.suptitle(test_fly_name , fontsize=12)


ax[0].plot(normal_data['timestamp'],normal_data['x'],color='r', label='Signal x')
ax[0].set_title('Signal x')

ax[1].plot(normal_data['timestamp'], normal_data['y'],color='r', label='Signal y')
ax[1].set_title('Signal y')

ax[2].plot(normal_data['timestamp'],normal_data['z'],color='r', label='Signal z')
ax[2].set_title('Signal z')


for ax in ax.flat:
    ax.set(xlabel='time in sec', ylabel='Amplitude')


print("\nFile analyse: " , f , '\n')


plt.show()




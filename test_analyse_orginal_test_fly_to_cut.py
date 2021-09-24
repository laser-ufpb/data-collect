import sys
import statistics
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

from scipy.signal import find_peaks

######## READ ME ###########
#Format : testfly_data.csv 		fx.x.x 		N
#
#the files are in folder test_fly_data and can be changed with the variable "cut_or_orginal"
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

test_fly_name = sys.argv[1]
cut_or_orginal= "cut_version"  #file directory 
#cut_or_orginal= "orginal"  #file directory 


with open('data_csv/test_fly_data/'+cut_or_orginal+'/'+ test_fly_name, 'rb') as f:
    clean_lines = (line.replace(b'\"',b'') for line in f)
    normal_data = np.genfromtxt(clean_lines,skip_header=1, delimiter=',',names=["x", "y", "z"])


#Figure Settings
fig, ax = plt.subplots(3,1, sharex=True, sharey=False)
fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=1.0)
fig.set_size_inches(10, 6, forward=True)
fig.suptitle(test_fly_name , fontsize=12)


#ValueError: x and y must have same first dimension, but have shapes (1,) and (75195,)
ax[0].plot(normal_data['x'],color='r', label='Signal x')
ax[0].set_title('Signal x')

ax[1].plot(normal_data['y'],color='r', label='Signal y')
#ax[1,0].plot(failure_data['y'],color='b', label='Failure y')
ax[1].set_title('Signal y')
# ax2.set_xlabel('x')
# ax2.set_ylabel('y')

ax[2].plot(normal_data['z'],color='r', label='Signal z')
#ax[2,0].plot(failure_data['z'],color='b', label='Failure z')
ax[2].set_title('Signal z')



for ax in ax.flat:
    ax.set(xlabel='n-Value', ylabel='Amplitude')

#Legend Settings
red_patch = mpatches.Patch(color='red', label= 'Good data')
blue_patch = mpatches.Patch(color='blue', label= 'Failure data')


print("#############################")



plt.show()




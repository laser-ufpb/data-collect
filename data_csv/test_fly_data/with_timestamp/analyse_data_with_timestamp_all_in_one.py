import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

from scipy.signal import find_peaks

######## READ ME ###########
#Format : 	N
#be sure you are in the right folder to run << data/csv/test_fly_data/with_timestemp >>
#the used files are in folder << test_fly_data/with_timestemp/drone_grande >> and can be changed with the variable "file_directory" line 36/37
#EX: d:/LASER/.venv/Scripts/python.exe analyse_data_with_timestamp_all_in_one.py 500
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


N = int(sys.argv[1]) # -> number of messurevalue interval 

#file_directory = "drone_grande/good_collection/"  #file directory 
file_directory = "drone_grande/bad_collection/"  #file directory 

#file = os.listdir("drone_grande") #just working when just files on folder "drone_grande" is (quick move from files can solve)
file = os.listdir(file_directory)
print(file)

N_string = 'N-Period = ' + str(N)
print(N_string) 

#Figure Settings
fig, ax = plt.subplots(3,1, sharex=True, sharey=False)
fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=1.0)
fig.set_size_inches(10, 6, forward=True)


for i in range(len(file)):
	
		fig.suptitle(file[i] , fontsize=12)
		
		with open(file_directory+file[i], 'rb') as f:
			normal_data = np.genfromtxt(f,skip_header=1, delimiter=',',names=['','timestamp','x', 'y','z'])


		ax[0].plot(normal_data['timestamp'], normal_data['x'], color='r', label='Signal x')
		ax[0].set_title('Signal x')

		ax[1].plot(normal_data['timestamp'], normal_data['y'], color='r', label='Signal y')
		ax[1].set_title('Signal y')

		ax[2].plot(normal_data['timestamp'],normal_data['z'], color='r', label='Signal z')
		ax[2].set_title('Signal z')


		print("\nFile analyse: " , f , '\n')

		
		changefile = '_' + str(N)

		try:
			os.makedirs('drone_grande/simple_anayse_images' + changefile +'/')
		except FileExistsError:
			pass

		plt.savefig('drone_grande/simple_anayse_images' + changefile +'/' + file[i] + '.png', dpi=150)

		
for ax in ax.flat:
    ax.set(ylabel='Amplitude')


#Legend Settings
red_patch = mpatches.Patch(color='red', label= 'Good data')
blue_patch = mpatches.Patch(color='blue', label= 'Failure data')
n_patch = mpatches.Circle(3, label= N_string)
legend = fig.legend(handles=[red_patch,blue_patch, n_patch], loc='upper right',bbox_to_anchor=(1.0, 1.0))
legend.get_frame().set_facecolor('C0')


#plt.show()
import sys
import os
import statistics
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

from scipy.signal import find_peaks

########READ ME ###########
#Format :	N
#the used files are in folder << test_fly_data/with_timestemp/drone_grande >> and can be changed with the variable "file_directory" line 41/42
#EX:  d:/LASER/.venv/Scripts/python.exe .\SAC_DM_compare_graph_for_csv_timestamp_all.py 500    
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

def plot_x (sec_value): 
	x1 = np.array(range(0, len(sec_value)))
	x1 = x1 * N
	
	return x1

N = int(sys.argv[1]) # -> number of messurevalue interval 
file_directory = "data_csv/test_fly_data/with_timestamp/drone_grande/good_collection/"
#file_directory = "data_csv/test_fly_data/with_timestamp/drone_grande/bad_collection/"
file = os.listdir(file_directory)

N_string = 'N-Period = ' + str(N)
print(N_string) 

failure_data_name = os.listdir("data_csv/simulated_failure_data")
print(failure_data_name)


for j in range(len(failure_data_name)):

	for i in range(len(file)):

		#Figure Settings
		fig, ax = plt.subplots(3, 2, sharex=False, sharey=False)
		fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.4, hspace=1.0)
		fig.set_size_inches(10, 6, forward=True)

		#Legend Settings
		red_patch = mpatches.Patch(color='red', label= 'Good data')
		blue_patch = mpatches.Patch(color='blue', label= 'Failure data')
		n_patch = mpatches.Circle(3, label= N_string)
		legend = fig.legend(handles=[red_patch,blue_patch, n_patch], loc='upper right',bbox_to_anchor=(1.0, 1.0))
		legend.get_frame().set_facecolor('C0')
		
	
		v_number = failure_data_name[j][4]
		n_number = failure_data_name[j][7]
	
		specialfileletter = failure_data_name[j][8]

		if specialfileletter == 'h':
			n_number = failure_data_name[j][7:9]
		else:
			pass 

		failure_file_name = str('data_csv/simulated_failure_data/' + failure_data_name[j][0:2] + '_v' + v_number + '_n' + n_number + '.csv')

		with open(failure_file_name, 'rb') as f1:
   	 		clean_lines = (line.replace(b'\"',b'') for line in f1)
   	 		failure_data = np.genfromtxt(clean_lines, skip_header=0, delimiter=',',names=["x", "y", "z"])
	

		with open(file_directory + file[i], 'rb') as f:
			normal_data = np.genfromtxt(f, skip_header=1, delimiter=',', names=['','timestamp','x', 'y','z'])
			

		fig.suptitle(file[i] + " compare with: " + failure_data_name[j][0:2] + '_v' + v_number + '_n' + n_number + '.csv', fontsize=12)

		print(file[i] + " compare with: " + failure_data_name[j][0:2] + '_v' + v_number + '_n' + n_number + '.csv')
	

		if (len(normal_data['x']) < len(failure_data['x']) ):
			menorTam = len(normal_data)
			diffrent =  len(failure_data['x'])-len(normal_data['x']) 
			failure_data = failure_data[:-diffrent]
		else:
			menorTam = len(failure_data)
			diffrent =  len(normal_data['x'])-len(failure_data['x']) 
			normal_data = normal_data[:-diffrent]


		sac_x_good = sac_dm(normal_data['x'], N, menorTam)
		sac_x_bad = sac_dm(failure_data['x'], N, menorTam)
		sac_y_good = sac_dm(normal_data['y'], N, menorTam)
		sac_y_bad = sac_dm(failure_data['y'], N, menorTam)
		sac_z_good = sac_dm(normal_data['z'], N, menorTam)
		sac_z_bad = sac_dm(failure_data['z'], N, menorTam)

		ax[0,0].plot(normal_data['timestamp'], normal_data['x'], color='r', label='Signal x')
		ax[0,0].plot(normal_data['timestamp'], failure_data['x'], color='b', label='Failure x')
		ax[0,0].set_title('Signal x')
		ax[0,0].set(xlabel='time in sec.', ylabel='Amplitude')

		ax[1,0].plot(normal_data['timestamp'], normal_data['y'], color='r', label='Signal y')
		ax[1,0].plot(normal_data['timestamp'], failure_data['y'], color='b', label='Failure y')
		ax[1,0].set_title('Signal y')
		ax[1,0].set(xlabel='time in sec.', ylabel='Amplitude')

		ax[2,0].plot(normal_data['timestamp'], normal_data['z'], color='r', label='Signal z')
		ax[2,0].plot(normal_data['timestamp'], failure_data['z'], color='b', label='Failure z')
		ax[2,0].set_title('Signal z')
		ax[2,0].set(xlabel='time in sec.', ylabel='Amplitude')

		ax[0,1].plot(plot_x(sac_x_good), sac_x_good, color='r', label='Good data')
		ax[0,1].plot(plot_x(sac_x_bad), sac_x_bad, color='b', label='Failure data')
		ax[0,1].set_title('SAC-DM X')
		ax[0,1].set(xlabel='n-value', ylabel='Amplitude')

		ax[1,1].plot(plot_x(sac_y_good), sac_y_good, color='r', label='Good data')
		ax[1,1].plot(plot_x(sac_y_bad), sac_y_bad, color='b', label='Failure data')
		ax[1,1].set_title('SAC-DM Y')
		ax[1,1].set(xlabel='n-value', ylabel='Amplitude')

		ax[2,1].plot(plot_x(sac_z_good), sac_z_good, color='r', label='Good data')
		ax[2,1].plot(plot_x(sac_z_bad), sac_z_bad, color='b', label='Failure data')
		ax[2,1].set_title('SAC-DM Z')
		ax[2,1].set(xlabel='n-value', ylabel='Amplitude')
		

		changefile = ""
		changefile = file[i][:-4] + '_' + str(N)
		print(changefile)

		try:
			os.makedirs('data_csv/test_fly_data/with_timestamp/drone_grande/images_compare_sac_dm'+'_'+file_directory[51]+'/' + changefile)
		except FileExistsError:
			pass

		plt.savefig('data_csv/test_fly_data/with_timestamp/drone_grande/images_compare_sac_dm'+'_'+file_directory[51]+'/' + changefile +  '/' + changefile + '_' + failure_data_name[j][0:2] + '_v' + v_number + '_n' + n_number + '.png', dpi=150)
		

		print("#############################")
		print('Diff media x: %.4f'%(statistics.fmean(sac_x_good)-statistics.fmean(sac_x_bad)))
		print('Diff media y: %.4f'%(statistics.fmean(sac_y_good)-statistics.fmean(sac_y_bad)))
		print('Diff media z: %.4f'%(statistics.fmean(sac_z_good)-statistics.fmean(sac_z_bad)))
		print("############################# \n")
		plt.cla()
		plt.clf()
		plt.close()
		


# Importing required python libraries
import numpy as np  
import matplotlib.cbook as cbook
import numpy
import sys

############ READ ME ####################
# Format : x.txt    y.txt   z.txt    resultfile.csv
#########################################

file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]

result_file = sys.argv[4]


a_file1 = np.genfromtxt(file1, delimiter='\n')
a_file2 = np.genfromtxt(file2, delimiter='\n')
a_file3 = np.genfromtxt(file3, delimiter='\n')


# with cbook.get_sample_data(file1) as file:
#     a_file1 = np.loadtxt(file)
# with cbook.get_sample_data(file2) as file:
#     a_file2 = np.loadtxt(file)
# with cbook.get_sample_data(file3) as file:
#     a_file3 = np.loadtxt(file)


a = np.c_[ a_file1, a_file2, a_file3 ] 

numpy.savetxt(result_file, a, fmt='%1.4f', delimiter = ",")

print("Merged ", file1, file2, file3, " into ", result_file )


#d:/LASER/hello/convertTXTtoCSV_argv.py .\data\Failure2\voo3\n1\x.txt .\data\Failure2\voo3\n1\y.txt .\data\Failure2\voo3\n1\z.txt .\data\Failure2\voo3\n1\f2_v3_n1.csv
#stop before Failure3
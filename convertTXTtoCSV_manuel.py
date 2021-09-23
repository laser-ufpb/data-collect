# Importing required python libraries
import numpy as np   
import matplotlib.cbook as cbook
import numpy

########
#Changes in the code 
########


# reading given csv file and creating dataframe
#nx = pd.read_csv("x.txt",header = 0, index_col=0)
#ny = pd.read_csv("y.txt",header = 1)


file1 = "D:/LASER/hello/data/Failure1/voo1/n2/x.txt"
file2 = "D:/LASER/hello/data/Failure1/voo1/n2/y.txt"
file3 = "D:/LASER/hello/data/Failure1/voo1/n2/z.txt"

result_file = "converted_file.csv"


with cbook.get_sample_data(file1) as file:
    a_file1 = np.loadtxt(file)
with cbook.get_sample_data(file2) as file:
    a_file2 = np.loadtxt(file)
with cbook.get_sample_data(file3) as file:
    a_file3 = np.loadtxt(file)


a = np.c_[ a_file1, a_file2, a_file3 ] 

#a.tofile('file.csv', sep = ',') #everything in one row
#pd.DataFrame(a).to_csv("file1.csv") # extra collums 

numpy.savetxt(result_file, a, fmt='%1.4f', delimiter = ",")

print("Merged ", file1, file2, file3, " into ", result_file )





########## Other methode but just read all and but all in CSV, not line by line ##########  

# import os
# import glob
# import pandas as pd
# os.chdir("D:/LASER/hello/data/Failure1/voo1/n1")

# extension = 'csv'
# all_filenames = [i for i in glob.glob('*.txt'.format(extension))]

# one_file = glob.glob('x.txt'.format(extension))
# second_file = glob.glob('y.txt'.format(extension))

# #combine all files in the list
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

# #export to csv
# combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
from contextlib import nullcontext
import sys
import numpy as np

import matplotlib.pyplot as plt

from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix

from scipy import signal
import scipy.interpolate #import interp1d
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
from scipy.signal import find_peaks, peak_prominences
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

def sac_am(data, N, menorTam):
    M = menorTam
    
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

axes = ['x','y','z']
N = 300
condition1 = sys.argv[1]
condition2 = sys.argv[2]
#condition3 = sys.argv[3]
#condition4 = sys.argv[4]

input1 = [[],[],[]]
input2 = [[],[],[]]
#input3 = [[],[],[]]
#input4 = [[],[],[]]
inputsLenth = []
#data1 = np.genfromtxt(file, delimiter=',', names=['t', 'x', 'y','z'])
#data2 = np.genfromtxt(file2, delimiter=',', names=['t', 'x', 'y','z'])


for i in range(3):
    
    file1 = '../'+'data/'+condition1+'/'+condition1+'_n'+sys.argv[3]+'_'+axes[i]+'.txt'
    file2 = '../'+'data/'+condition2+'/'+condition2+'_n'+sys.argv[3]+'_'+axes[i]+'.txt'
    #file3 = '../'+'data/'+condition3+'/'+condition3+'_n'+sys.argv[5]+'_'+axes[i]+'.txt'
    #file4 = '../'+'data/'+condition4+'/'+condition4+'_n'+sys.argv[5]+'_'+axes[i]+'.txt'
    

    data1 = np.genfromtxt(file1, delimiter='\n', names=['z'])
    inputsLenth.append(len(data1))
    data2 = np.genfromtxt(file2, delimiter='\n', names=['z'])
    inputsLenth.append(len(data2))
    #data3 = np.genfromtxt(file3, delimiter='\n', names=['z'])
    #inputsLenth.append(len(data3))
    #data4 = np.genfromtxt(file4, delimiter='\n', names=['z'])
    #inputsLenth.append(len(data4))

    menorTam = min(inputsLenth)
   
    sac = sac_dm(data1, N, menorTam)
    sac2 = sac_dm(data2, N, menorTam)
    #sac3 = sac_dm(data3,N,menorTam)
    #sac4 = sac_dm(data4,N,menorTam)
    
    input1[i] = sac
    input2[i] = sac2
    #input3[i] = sac3
    #input4[i] = sac4
    #input1[i] = data1
    #input2[i] = data2
    
#X = np.concatenate((np.array(input1).T, np.array(input2).T,np.array(input3).T,np.array(input4).T))
X = np.concatenate((np.array(input1).T, np.array(input2).T)) 
X = X.astype(np.float64)
menorTam = len(np.array(input2).T) 


y = []

for i in range(len(X)):
    if(i<menorTam):
        y.append(0)
    elif((i >= menorTam) and (i < (menorTam*2))):
        y.append(1)
    """ elif((i >= (menorTam*2)) and (i < (menorTam*3))):
        y.append(1)
    else:
        y.append(1)
    """

y = np.array(y)
class_names = ['Nominal','Failure']




# Split the data into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Run classifier, using a model that is too regularized (C too low) to see
# the impact on the results
#classifier = svm.SVC(kernel='linear', C=0.01).fit(X_train, y_train)
#classifier = KNeighborsClassifier(2).fit(X_train, y_train)
#classifier = MLPClassifier(alpha=1, max_iter=1000).fit(X_train, y_train)

# Classificadores 

#classifier = KNeighborsClassifier(3).fit(X_train, y_train)

#classifier = svm.SVC(kernel="linear", C=0.025).fit(X_train, y_train)

#classifier = svm.SVC(gamma=2, C=0.1).fit(X_train, y_train)

#classifier = GaussianProcessClassifier(1.0 * RBF(1.0)).fit(X_train, y_train)

#classifier = DecisionTreeClassifier(max_depth=5).fit(X_train, y_train)


classifier = RandomForestClassifier(n_estimators=100, criterion="entropy").fit(X_train, y_train)

#classifier = MLPClassifier(alpha=1, max_iter=1000).fit(X_train, y_train)

#classifier = AdaBoostClassifier(n_estimators=100,learning_rate=0.5).fit(X_train, y_train) #esse ta melhor

#classifier = GaussianNB().fit(X_train, y_train)

#classifier = QuadraticDiscriminantAnalysis().fit(X_train, y_train)


np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]



for title, normalize in titles_options:
    disp = plot_confusion_matrix(classifier, X_test, y_test,
                                 display_labels=class_names,
                                 cmap=plt.cm.Blues,
                                 normalize=normalize)
    disp.ax_.set_title(title)

    print(title)
    print(disp.confusion_matrix)

    if (title == "Confusion matrix, without normalization"):
        cfm = disp.confusion_matrix

acuracia = ((cfm[0][0]+cfm[1][1])/cfm.sum())*100
print("acuracia: ",acuracia,"%")

plt.show()
 
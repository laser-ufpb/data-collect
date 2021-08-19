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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier

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


N = int(sys.argv[3])
file1 = sys.argv[1]
file2 = sys.argv[2]

#data1 = np.genfromtxt(file, delimiter=',', names=['t', 'x', 'y','z'])
#data2 = np.genfromtxt(file2, delimiter=',', names=['t', 'x', 'y','z'])
data1 = np.genfromtxt(file1, delimiter='\n', names=['z'])
data2 = np.genfromtxt(file2, delimiter='\n', names=['z'])

if (len(data1) < len(data2) ):
	menorTam = len(data1)
else:
	menorTam = len(data2)

#menorTam = len(data1)
sac = sac_am(data1, N, menorTam)

#menorTam = len(data2)
sac2 = sac_am(data2, N, menorTam)

X = np.reshape(np.array(sac+sac2), (-1, 1))

y = []


for i in range(len(X)):
    if(i<(len(X)/2)):
        y.append(0)
    else:
        y.append(1)
y = np.array(y)
class_names = ['Nominal','Failure']




# Split the data into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

print(X_train)
print(y_train)
# Run classifier, using a model that is too regularized (C too low) to see
# the impact on the results
#classifier = svm.SVC(kernel='linear', C=0.01).fit(X_train, y_train)
classifier = KNeighborsClassifier(2).fit(X_train, y_train)
#classifier = MLPClassifier(alpha=1, max_iter=1000).fit(X_train, y_train)

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

plt.show()

from sklearn.datasets import load_iris
data = load_iris()
data.target[[10, 25, 50]]
#array([0, 0, 1])
print(data)
#print(list(data.target_names))

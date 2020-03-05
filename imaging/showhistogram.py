import numpy as np
import pickle
import matplotlib.pyplot as plt

with open("/home/niki/hoge/fileupload/static/sum","rb") as f:
    d = pickle.load(f)

result = []
for i in range(0,24):
    #result[i] = d[i+1] - d[i]
    print(d[i])
#x = np.arange(0,22,1)
#plt.plot(x,result)
#plt.show()


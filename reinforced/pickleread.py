import pickle
import numpy as np

with open("qtable","rb") as f:
    a = pickle.load(f)

a = np.append(a,1)

print(a)


with open("qtable","wb") as f:
    pickle.dump(a,f)


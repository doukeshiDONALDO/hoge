import pickle
import numpy

with open("qtable","rb") as f:
    a = pickle.load(f)
    
print(a)

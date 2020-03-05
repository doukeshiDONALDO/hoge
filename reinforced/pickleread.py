import pickle
import numpy as np

class QQ():
    def __init__(self):
        self.qtable = np.zeros((8,8),dtype="uint64")
        self.state = 0
        self.action = 0
        self.turn = 0
        self.trying = [0,0,0,0,0,0,0,0]



with open("sum","rb") as f:
    a = pickle.load(f)

#a = np.append(a,1)
for i in a:
    print(i)



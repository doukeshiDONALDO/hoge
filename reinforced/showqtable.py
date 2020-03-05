import pickle
import numpy as np


class QQ():
    def __init__(self):
        self.qtable = np.zeros((8,8))
        self.state = 0
        self.action = 0
        self.turn = 1
        self.trying = [0,0,0,0,0,0,0,0]



with open("ini_qtable","rb") as f:
    qq = pickle.load(f)



print(qq.qtable)




import pickle
import numpy


class QQ():
    def __init__(self):
        self.qtable = numpy.zeros((8,8)) 
        self.state = None


if __name__=="__main__":
    test = QQ()
    with open("qtable","wb") as f:
        pickle.dump(test,f)

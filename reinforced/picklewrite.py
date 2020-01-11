import pickle
import numpy


class QQ():
    def __init__(self):
        self.qtable = numpy.zeros((8,8)) 
        self.state = None


if __name__=="__main__":
    test = QQ()
    a = []
    with open("sum","wb") as f:
        pickle.dump(a,f)

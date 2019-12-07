import numpy as np

def get_action(_q_table):
    epsilon = 0.02
    if np.random.uniform(0, 1) > epsilon:
        _action = np.argmax(_q_table)
    else:
        _action = np.random.choice([0,1,2,3,4,5,6,7])
    return _action



if __name__ == '__main__':
    _q_table = np.zeros((8,8))

    action = get_action(_q_table)

    print(action)

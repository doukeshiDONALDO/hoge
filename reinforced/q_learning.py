#!/usr/bin/env python
# coding: UTF-8

import numpy as np
from time import sleep
import sqlite3
import sys
from sys import argv
import pickle

class QQ():
    def __init__(self):
        self.qtable = np.zeros((8,8))
        self.state = None
        self.action = None

"""    def state(self):
        return self.state

    def set_state(self,value):
        self.state = value
    
    def action(self):
        return self.action

    def set_action(self,value):
        self.action = value
   """     


def get_action(_q_table):
    epsilon = 0.002
    if np.random.uniform(0, 1) > epsilon:
        _action = np.argmax(_q_table[qq.action])
    else:
        _action = np.random.choice([0,1,2,3,4,5,6,7])
    return _action




def update_q_table(_q_table, _action, _reward):

    alpha = 0.2 # 学習率
    gamma = 0.99# 時間割引き率

    # 行動後の状態で得られる最大行動価値 Q(s',a')
    next_max_q_value = max(_q_table[qq.action])

    # 行動前の状態の行動価値 Q(s,a)
    q_value = _q_table[qq.state][qq.action]

    # 行動価値関数の更新
    # q(s,a) = q(s,a) + α(R(s,a) + γmaxq(s',a') - q(s,a))
    _q_table[qq.state][qq.action] = q_value + alpha * (_reward + gamma * next_max_q_value - q_value)


if __name__ == '__main__':

    if sys.argv[1] == 'init':
        qq = QQ()
        qq.state = 0
        qq.action = get_action(qq.qtable)
        with open("qtable","wb") as f:
            pickle.dump(qq,f)
        sys.exit()
    else:
        with open("qtable","rb") as f:
            qq = pickle.load(f)

        reward = int(sys.argv[1])

        
        # ε-グリーディ法で行動を選択
        action = get_action(qq.qtable)
        print('action: {}'.format(action))

        # Qテーブルの更新
        update_q_table(qq.qtable, action, reward)

        print(qq.qtable)
        qq.state = qq.action
        qq.action = action

    with open("qtable","wb") as f:
        pickle.dump(qq,f)
    

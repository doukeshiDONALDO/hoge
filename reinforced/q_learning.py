#!/usr/bin/env python
# coding: UTF-8

import numpy as np
from time import sleep
import sqlite3
import sys
from sys import argv
import pickle
import socket
light = [
b'0,0,0,0',
b'255,0,0,255',
b'0,255,0,255',
b'0,0,255,255',
b'0,255,255,255',
b'255,0,255,255',
b'255,255,0,255',
b'255,255,255,255'
]

class QQ():
    def __init__(self):
        self.qtable = np.zeros((8,8))
        self.state = 0
        self.action = 0
        self.turn = 1
        self.trying = [0,0,0,0,0,0,0,0]

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
    epsilon = 0.5
    if qq.turn < 8:
        _action = qq.turn
    elif np.random.uniform(0, 1) > epsilon:
        _action = np.argmax(_q_table[qq.action])
    else:
        _action = np.random.choice([0,1,2,3,4,5,6,7])
    qq.trying[_action] += 1
    return _action




def update_q_table(_q_table, _reward):

    alpha = 0.9 # 学習率
    gamma = 0.1# 時間割引き率

    # 行動後の状態で得られる最大行動価値 Q(s',a')
    next_max_q_value = max(_q_table[qq.action])

    # 行動前の状態の行動価値 Q(s,a)
    q_value = _q_table[qq.state][qq.action]

    # 行動価値関数の更新
    # q(s,a) = q(s,a) + α(R(s,a) + γmaxq(s',a') - q(s,a))
    _q_table[qq.state][qq.action] = q_value + alpha * (_reward + gamma * next_max_q_value - q_value)
 
    print("{}, {}, {}".format(_q_table[qq.state][qq.action],next_max_q_value,q_value,))

if __name__ == '__main__':

    if sys.argv[1] == 'init':
        qq = QQ()
        qq.action = get_action(qq.qtable)
        with open("qtable","wb") as f:
            pickle.dump(qq,f)
        sys.exit()
    else:
        with open("qtable","rb") as f:
            qq = pickle.load(f)

        reward = int(sys.argv[1])
        print('turn: {}'.format(qq.turn))
        print('tring: {}'.format(qq.trying)) 
        # ε-グリーディ法で行動を選択
        action = get_action(qq.qtable)
        print('action: {}'.format(action))

        # Qテーブルの更新
        update_q_table(qq.qtable, reward)

        print("state: {},action: {}".format(qq.state,qq.action))
        print(qq.qtable)
        qq.state = qq.action
        qq.action = action
        qq.turn += 1
        print("state': {},action': {}".format(qq.state,qq.action))



        target_host = '192.168.73.50'
        target_port = 9999
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        client.connect((target_host,target_port))
        
        client.send(light[qq.action])
        
        response = client.recv(4096)
        client.close()
        print(response)


    with open("qtable","wb") as f:
        pickle.dump(qq,f)
    

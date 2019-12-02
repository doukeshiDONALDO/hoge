#!/usr/bin/env python
# coding: UTF-8

import numpy as np
from time import sleep
import sqlite3

def get_status():
    state = np.random.uniform(0, 10)
    return state

def get_action(_q_table):
    epsilon = 0.002
    if np.random.uniform(0, 1) > epsilon:
        state = get_status()
        _action = np.argmax(_q_table[state])
    else:
        _action = np.random.choice([0, 1, 2])
    return _action

def get_reward():



    return 

def update_q_table(_q_table, _action, _reward):

    alpha = 0.2 # 学習率
    gamma = 0.99# 時間割引き率

    # 行動後の状態で得られる最大行動価値 Q(s',a')
    next_position, next_velocity = get_status()
    next_max_q_value = max(_q_table[next_position][next_velocity])

    # 行動前の状態の行動価値 Q(s,a)
    state = get_status()
    q_value = _q_table[state][_action]

    # 行動価値関数の更新
    # q(s,a) = q(s,a) + α(R(s,a) + γmaxq(s',a') - q(s,a))
    _q_table[position][velocity][_action] = q_value + alpha * (_reward + gamma * next_max_q_value - q_value)

    return _q_table

if __name__ == '__main__':


    # Qテーブルの初期化
    q_table = np.zeros((8, 8))

    rewards = []


        
    # ε-グリーディ法で行動を選択
    action = get_action(q_table)

    # 車を動かし、観測結果・報酬・ゲーム終了FLG・詳細情報を取得
    reward = get_reward()


    # Qテーブルの更新
    q_table = update_q_table(q_table, action, observation, next_observation, reward, episode)




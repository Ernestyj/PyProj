# -*- coding: utf-8 -*-

__author__ = 'DCLab'

import random
import math

# The dorms, each of which has two available spaces
dorms = ['Zeus', 'Athena', 'Hercules', 'Bacchus', 'Pluto']

# People, along with their first and second choices
prefs = [('Toby', ('Bacchus', 'Hercules')),
         ('Steve', ('Zeus', 'Pluto')),
         ('Karen', ('Athena', 'Zeus')),
         ('Sarah', ('Zeus', 'Pluto')),
         ('Dave', ('Athena', 'Bacchus')),
         ('Jeff', ('Hercules', 'Pluto')),
         ('Fred', ('Pluto', 'Athena')),
         ('Suzie', ('Bacchus', 'Hercules')),
         ('Laura', ('Bacchus', 'Hercules')),
         ('James', ('Hercules', 'Athena'))]

# [(0,9),(0,8),(0,7),(0,6),...,(0,0)]
domain = [(0, (len(dorms) * 2) - i - 1) for i in range(0, len(dorms) * 2)]


# Description: 将数字序列的题解转换为宿舍分配表
def printSolution(vec):
    slots = []
    # 建立一个槽序列，每个宿舍两个槽
    for i in range(len(dorms)): slots += [i, i]
    # 遍历每一名学生的安置情况
    for i in range(len(vec)):
        x = int(vec[i])
        # 从剩余槽中选择
        dorm = dorms[slots[x]]
        # 输出学生及其被分配的宿舍
        print prefs[i][0], dorm
        # 删除该槽
        del slots[x]

print('测试：将数字序列的题解转换为宿舍分配表')
vec = [7, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# printSolution(vec)
print('****************************************************************************************')


# Description: 宿舍分配成本函数
def dormCost(vec):
    cost=0
    slots = []
    # 建立一个槽序列，每个宿舍两个槽
    for i in range(len(dorms)): slots += [i, i]
    # 遍历每一个学生
    for i in range(len(vec)):
        x=int(vec[i])
        dorm=dorms[slots[x]]
        pref=prefs[i][1]
        # 首选成本=0，次选=1，不在选择项=3
        if pref[0]==dorm: cost+=0
        elif pref[1]==dorm: cost+=1
        else: cost+=3
        # 删除选中的槽
        del slots[x]
    return cost

from optimization import randomOptimize, geneticOptimize

print('随机搜索宿舍问题的最优题解，默认1000次猜测')
s=randomOptimize(domain, dormCost)
printSolution(s)
print('遗传算法搜索宿舍问题的最优题解，popsize=50, step=1, mutprob=0.2, elite=0.2, maxiter=100')
s=geneticOptimize(domain, dormCost)
printSolution(s)
print('****************************************************************************************')


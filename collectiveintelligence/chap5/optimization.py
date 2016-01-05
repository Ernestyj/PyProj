# -*- coding: utf-8 -*-

__author__ = 'DCLab'

import time, random, math

# 人员定义
people = [('Seymour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zooey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]
# 纽约的Laguardia机场
destination = 'LGA'

print('读入航班数据')
flights = {}
for line in file('schedule.txt'):
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights.setdefault((origin, dest), [])
    # Add details to the list of possible flights
    flights[(origin, dest)].append((depart, arrive, int(price)))
print('****************************************************************************************')


# Description: 获取分钟数
def getMinutes(t):
    x=time.strptime(t, '%H:%M')
    return x[3]*60+x[4]


# Description: 将数字序列的题解转换为航班表格
def printSchedule(r):
    for d in range(len(r) / 2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][int(r[d * 2])]
        ret = flights[(destination, origin)][int(r[d * 2 + 1])]
        print '%10s%10s %8s-%5s  $%3s %8s-%5s  $%3s' % \
              (name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2])

print('测试：将数字序列的题解s转换为航班表格')
solutions = [1,4,3,2,7,3,6,3,2,4,5,3]
printSchedule(solutions)
print('****************************************************************************************')


# Description: 计算旅行成本函数
# Output: 返回值越大则方案越差
def scheduleCost(sol):
    latestarrival = 0
    earliestdep = 24 * 60

    totalprice = 0
    for d in range(len(sol) / 2):
        # Get the return and outbound flights
        origin = people[d][1]
        outboundF = flights[(origin, destination)][int(sol[d * 2])]
        returnF = flights[(destination, origin)][int(sol[d * 2 + 1])]
        # Total price is the price of all outbound and return flights
        totalprice += outboundF[2]
        totalprice += returnF[2]
        # Track the latest arrival and earliest departure
        if latestarrival < getMinutes(outboundF[1]): latestarrival = getMinutes(outboundF[1])
        if earliestdep > getMinutes(returnF[0]): earliestdep = getMinutes(returnF[0])
    # Every person must wait at the airport until the latest person arrives.
    # They also must arrive at the same time and wait for their flights.
    totalwait = 0
    for d in range(len(sol) / 2):
        origin = people[d][1]
        outboundF = flights[(origin, destination)][int(sol[d * 2])]
        returnF = flights[(destination, origin)][int(sol[d * 2 + 1])]
        totalwait += latestarrival - getMinutes(outboundF[1])
        totalwait += getMinutes(returnF[0]) - earliestdep

    # Does this solution require an extra day of car rental? That'll be $50!
    if latestarrival < earliestdep: totalprice += 50

    return totalprice + totalwait

print('测试：按题解s计算旅行成本')
solutions = [1,4,3,2,7,3,6,3,2,4,5,3]
print(scheduleCost(solutions))
print('****************************************************************************************')


# Description: 随机搜索函数（默认1000次猜测）
# Input: domain是由二元组构成的列表，指定题解中每个变量的最小最大值；题解长度与此列表长度相同
#       costFunction是成本函数
def randomOptimize(domain, costFunction):
    best=999999999
    bestr=None
    for i in range(1000):
        # 创建一个随机解
        r=[ random.randint(domain[i][0], domain[i][1]) for i in range(len(domain)) ]
        # 得到成本
        cost=costFunction(r)
        # 与到目前为止的最优解进行比较
        if cost<best:
            best=cost
            bestr=r
    print 'best cost: %d' % best
    return bestr

print('随机搜索旅行安排问题的最优题解，默认1000次猜测')
domain=[(0, 9)] * (len(people)*2)
solutions=randomOptimize(domain, scheduleCost)
printSchedule(solutions)
print('****************************************************************************************')





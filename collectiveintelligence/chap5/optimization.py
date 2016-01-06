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
solution = [1,4,3,2,7,3,6,3,2,4,5,3]
# printSchedule(solution)
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
print(scheduleCost(solution))
print('****************************************************************************************')


# Description: 随机搜索优化函数（默认1000次猜测）
# Input: domain是由二元组构成的列表，指定题解中每个变量的最小最大值；题解长度与此列表长度相同
#       costFunction是成本函数
def randomOptimize(domain, costFunction):
    best=999999999
    bestr=None
    for i in range(1000):
        # 创建随机解
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
solution=randomOptimize(domain, scheduleCost)
printSchedule(solution)
print('****************************************************************************************')


# Description: 爬山法搜索优化函数
def hillClimb(domain, costFunction):
    # 创建一个随机解
    sol=[ random.randint(domain[i][0], domain[i][1]) for i in range(len(domain)) ]
    # 主循环
    while 1:
        # 创建相邻解的列表
        neighbors=[]
        for j in range(len(domain)):
            # 在每个方向上相对于原值偏离一点
            if sol[j]>domain[j][0]:
                neighbors.append(sol[0:j] + [sol[j]-1] + sol[j+1:])
            if sol[j]<domain[j][1]:
                neighbors.append(sol[0:j] + [sol[j]+1] + sol[j+1:])
        # 在相邻解中寻找最优解
        current=costFunction(sol)
        best=current
        for j in range(len(neighbors)):
            cost=costFunction(neighbors[j])
            if cost<best:
                best=cost
                sol=neighbors[j]
        # 如果没有更好的解，则退出循环
        if best==current: break
    print 'best cost: %d' % best
    return sol

print('爬山法搜索旅行安排问题的最优题解')
solution=hillClimb(domain, scheduleCost)
printSchedule(solution)
print('****************************************************************************************')


# Description: 模拟退火算法，默认T=10000.0, cool=0.95, step=1
#       其中接受更高成本题解的概率p=pow(math.e, -(costB-cost)/T),p随着降火从接近1下降到接近0
def annealingOptimize(domain, costFunction, T=10000.0, cool=0.95, step=1):
    # 随机初始化值
    vec=[ random.randint(domain[i][0], domain[i][1]) for i in range(len(domain)) ]
    while T>0.1:
        # 随机选择一个索引
        i=random.randint(0, len(domain)-1)
        # 随机选择一个改变索引值的方向
        direction=random.randint(-step, step)
        # 创建一个代表题解的新列表（深度复制），并改变其中一个值
        vecB=vec[:]
        vecB[i]+=direction
        if vecB[i]<domain[i][0]: vecB[i]=domain[i][0]
        elif vecB[i]>domain[i][1]: vecB[i]=domain[i][1]
        # 计算当前成本和新的成本
        cost=costFunction(vec)
        costB=costFunction(vecB)
        best=cost
        # 是更好的解吗？或者是趋向最优解的可能临界解吗？
        if (costB<cost or random.random()<pow(math.e, -(costB-cost)/T)):
            vec=vecB
            best=costB
        # 降低温度
        T=T*cool
    print 'best cost: %d' % best
    return vec

print('模拟退火算法搜索旅行安排问题的最优题解，T=10000.0, cool=0.95, step=1')
solution=annealingOptimize(domain, scheduleCost)
printSchedule(solution)
print('****************************************************************************************')


# Description: 遗传算法，默认popsize=50, step=1, mutprob=0.2, elite=0.2, maxiter=100
def geneticOptimize(domain, costFunction, popsize=50, step=1,
                    mutprob=0.2, elite=0.2, maxiter=100):
    # 变异操作
    def mutate(vec):
        i=random.randint(0, len(domain)-1)
        if random.random()<0.5 and vec[i]>domain[i][0]:
            return vec[0:i] + [vec[i]-step] + vec[i+1:]
        elif vec[i]<domain[i][1]:
            return vec[0:i] + [vec[i]+step] + vec[i+1:]

    # 交叉操作
    def crossover(r1, r2):
        i=random.randint(1, len(domain)-2)
        return r1[0:i] + r2[i:]

    # 构造初始种群
    pop=[]
    for i in range(popsize):
        vec=[ random.randint(domain[i][0], domain[i][1]) for i in range(len(domain)) ]
        pop.append(vec)
    # 每一代中有多少胜出者
    topElite=int(elite*popsize)
    # 主循环
    for i in range(maxiter):
        scores=[ (costFunction(v), v) for v in pop if v!=None ]
        scores.sort()
        ranked=[ v for (s, v) in scores ]
        # 从纯粹的胜出者开始
        pop=ranked[0:topElite]
        # 添加变异和配对后的胜出者
        while len(pop)<popsize:
            if random.random()<mutprob:
                # 变异
                c=random.randint(0, topElite)
                pop.append(mutate(ranked[c]))
            else:
                # 交叉
                c1=random.randint(0, topElite)
                c2=random.randint(0, topElite)
                pop.append(crossover(ranked[c1], ranked[c2]))
        # 打印当前最优值
        # print scores[0][0]
    print scores[0][0]
    return scores[0][1]

print('遗传算法搜索旅行安排问题的最优题解，popsize=50, step=1, mutprob=0.2, elite=0.2, maxiter=100')
solution=geneticOptimize(domain, scheduleCost)
printSchedule(solution)
print('****************************************************************************************')



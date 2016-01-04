# -*- coding: utf-8 -*-

__author__ = 'DCLab'

# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},

           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},

           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},

           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},

           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},

           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},

           'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}


from math import sqrt


# Description: 寻找相近的用户，求欧几里得距离评价
# Output: 0~1, 1表示两人具有一样的偏好
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    # if they have no ratings in common, return 0
    if len(si)==0:
        return 0
    # Add up the squares of all the differences
    sum_of_squares=sum( [ pow(prefs[person1][item] - prefs[person2][item], 2)
                        for item in prefs[person1] if item in prefs[person2] ] )

    return 1 / (1 + sqrt(sum_of_squares))

print('Lisa Rose与Gene Seymour的相似度（欧几里得距离）')
result = sim_distance(critics, 'Lisa Rose', 'Gene Seymour')
print(result)
print('****************************************************************************************')


# Description: 寻找相近的用户，求皮尔逊相关系数因子（Pearson correlation coefficient）
# Output: -1~1，1表示两人对每一样物品均有一致的评价
def sim_pearson(prefs, p1, p2):
    # 得到双方都曾评价过的物品列表
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
    # 如果两者没有共同之处，则返回1
    n=len(si)
    if n==0: return 1
    # 对所有偏好求和
    sum1=sum( [prefs[p1][it] for it in si] )
    sum2=sum( [prefs[p2][it] for it in si] )
    # 求平方和
    sum1Sq=sum( [pow(prefs[p1][it], 2) for it in si] )
    sum2Sq=sum( [pow(prefs[p2][it], 2) for it in si] )
    # 求乘积之和
    pSum=sum( [prefs[p1][it]*prefs[p2][it] for it in si] )
    # 计算皮尔逊评价值（相关系数因子）
    num=pSum-(sum1*sum2/n)
    den=sqrt( (sum1Sq-pow(sum1, 2)/n)*(sum2Sq-pow(sum2, 2)/n) )
    if den==0: return 0

    r=num/den
    return r

print('Lisa Rose与Gene Seymour的相似度（皮尔逊相关系数因子）')
result = sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
print(result)
print('****************************************************************************************')


# Description: 计算与所有人的相似度，返回最相似的前n个值
# Output:
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores=[ (similarity(prefs, person, other), other) for other in prefs if other!=person ]
    # 排序
    scores.sort()
    scores.reverse()
    return scores[0:n]

print('与Lisa Rose相似的前5个用户')
result = topMatches(critics, 'Lisa Rose')
print(result)
print('****************************************************************************************')


# Description: 推荐物品（影片），利用所有其他人打分的加权平均，为某人提供推荐
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        # 忽略与自己的比较
        if other==person: continue
        # 计算相似值
        sim=similarity(prefs, person, other)
        # 忽略相似值不大于0的情况
        if sim<=0: continue

        for item in prefs[other]:
            # 只对自己还没看过的影片进行评价
            if item not in prefs[person] or prefs[person][item]==0:
                # 相似度*评分
                totals.setdefault(item, 0)
                totals[item]+=prefs[other][item]*sim
                # 相似度之和
                simSums.setdefault(item, 0)
                simSums[item]+=sim
    # 建立归一化列表
    rankings=[ (total/simSums[item], item) for item, total in totals.items() ]

    rankings.sort()
    rankings.reverse()
    return rankings

print('为Toby推荐影片（皮尔逊相关系数）')
result = getRecommendations(critics, 'Toby')
print(result)
print('为Toby推荐影片（基于欧几里德距离）')
result = getRecommendations(critics, 'Toby', similarity=sim_distance)
print(result)
print('****************************************************************************************')


# Description: 偏好数据对象转换，用以之后计算物品的相似值（匹配物品）
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # 将物品和人员对调
            result[item][person]=prefs[person][item]
    return result

print('影片数据集')
movies = transformPrefs(critics)
print(movies)
print('推荐与《Superman Returns》相似的影片（前5）')
result = topMatches(movies, 'Superman Returns')
print(result)
print('为影片《Just My Luck》推荐评分者')
result = getRecommendations(movies, 'Just My Luck')
print(result)
print('****************************************************************************************')


# Description：构造物品比较数据集（相似度采用sim_distance计算）
# Output: 返回包含物品及其最相近物品列表的字典
def calculateSimilarItems(prefs, n=10):
    result={}
    itemPrefs = transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        # 针对大数据集更新状态变量
        c+=1
        if c%100 == 0: print("%d / %d" % (c, len(itemPrefs)))
        # 寻找最为相近的物品
        scores=topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item]=scores
    return result

print('建立影片及其相似影片字典（前10个）')
itemsim=calculateSimilarItems(critics)
print(itemsim)
print('****************************************************************************************')


# Description:
def getRecommendedItems(prefs, itemMatch, user):
    userRatings=prefs[user]
    scores={}
    totalSim={}
    # 循环遍历由当前用户评分的物品
    for (item, rating) in userRatings.items():
        # 循环遍历与当前物品相近的物品
        for (similarity, item2) in itemMatch[item]:
            # 如果该用户已经对当前物品评价过，则忽略
            if item2 in userRatings: continue
            # 评价值与相似度的加权和
            scores.setdefault(item2, 0)
            scores[item2]+=similarity*rating
            # 全部相似度之和
            totalSim.setdefault(item2, 0)
            totalSim[item2]+=similarity
    # 将每个合计值除以加权和，求出平均值
    rankings=[ (score/totalSim[item], item) for item, score in scores.items() ]

    rankings.sort()
    rankings.reverse()
    return rankings

print('推荐给Toby的影片')
result=getRecommendedItems(critics, itemsim, 'Toby')
print(result)
print('****************************************************************************************')


# Description:
def loadMovieLens(path='./'):
    # 获取影片标题
    movies={}
    for line in open(path+'u.item'):
        (id, title)=line.split('|')[0:2]
        movies[id]=title
    # 加载数据
    prefs={}
    for line in open(path+'u.data'):
        (user, movieid, rating, ts)=line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]]=float(rating)
    return prefs

print('加载MovieLens数据，打印user=88的数据')
prefs=loadMovieLens()
print(prefs['88'])
print('****************************************************************************************')


print('基于用户的协同过滤：为用户87推荐影片（前30部）')
result=getRecommendations(prefs, '87')[0:30]
print(result)
print('基于物品的协同过滤：建立影片及其相似影片字典（前50个）(注意：此步非常耗时！)')
# itemsim=calculateSimilarItems(prefs, n=50)
# print(itemsim)
print('基于物品的协同过滤：为用户87推荐影片（前30部）')
# result=getRecommendedItems(prefs, itemsim, '87')[0:30]
# print(result)
print('****************************************************************************************')







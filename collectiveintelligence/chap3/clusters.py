# -*- coding: utf-8 -*-

__author__ = 'DCLab'


# Description: 加载博客数据
def readfile(filename):
    lines = [line for line in file(filename)]
    # 第一行是列标题
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # 每行第一列是行名
        rownames.append(p[0])
        # 剩余部分是该行对应的数据
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


from math import sqrt


# Description: 计算与皮尔逊相关系数相关的距离值
# Output: 1.0减去皮尔逊相关度后的值，为了让相似度越大的两个元素间距离更小
def pearson(v1, v2):
    # 简单求和
    sum1 = sum(v1)
    sum2 = sum(v2)
    # 求平方和
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])
    # 求乘积之和
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])
    # 计算r
    numerator = pSum - (sum1 * sum2 / len(v1))
    denominator = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if denominator == 0: return 0
    r = numerator / denominator

    return 1.0 - r


# 定义分级聚类中的聚类类型
class Bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id


# Description: 分级聚类算法
def hcluster(rows, distance=pearson):
    distances = {}
    currentClusterId = -1
    # 最开始的聚类就是数据集中的行
    clusts = [Bicluster(rows[i], id=i) for i in range(len(rows))]
    while len(clusts) > 1:
        lowestPair = (0, 1)
        closest = distance(clusts[0].vec, clusts[1].vec)
        # 遍历每一个配对，寻找最小距离
        for i in range(len(clusts)):
            for j in range(i + 1, len(clusts)):
                # 用distances缓存距离的计算值
                if (clusts[i].id, clusts[j].id) not in distances:
                    distances[(clusts[i].id, clusts[j].id)] = distance(clusts[i].vec, clusts[j].vec)
                d = distances[(clusts[i].id, clusts[j].id)]
                if d < closest:
                    closest = d
                    lowestPair = (i, j)
        # 计算两个聚类的均值
        mergeVec = [(clusts[lowestPair[0]].vec[i] + clusts[lowestPair[1]].vec[i]) / 2.0
                    for i in range(len(clusts[0].vec))]
        # 建立新的聚类
        newCluster = Bicluster(mergeVec, left=clusts[lowestPair[0]], right=clusts[lowestPair[1]],
                               distance=closest, id=currentClusterId)
        # 不在原始集合中的聚类，其id为负数
        currentClusterId -= 1
        del clusts[lowestPair[1]]
        del clusts[lowestPair[0]]
        clusts.append(newCluster)

    return clusts[0]


print('按博客进行聚类（分级行聚类）')
blogNames, words, data = readfile('blogdata.txt')
clust = hcluster(data)
print('****************************************************************************************')


# Description: 打印聚类结果(树形结构)
def printClusts(clust, labels=None, n=0):
    # 利用缩进来建立层级布局
    for i in range(n): print(' '),
    if clust.id < 0:
        # 负数标记代表这是一个分支
        print('-')
    else:
        # 正数标记代表这是一个叶节点
        if labels == None: print(clust.id)
        else: print(labels[clust.id])
    # 打印右侧分支和左侧分支
    if clust.left != None: printClusts(clust.left, labels=labels, n=n+1)
    if clust.right != None: printClusts(clust.right, labels=labels, n=n+1)


print('打印聚类结果')
# printClusts(clust, labels=blogNames)
print('****************************************************************************************')


from PIL import Image, ImageDraw

# Description: 确定聚类的总体高度
def getHeight(clust):
    # 叶节点高度为1
    if clust.left==None and clust.right==None: return 1
    # 否则高度为每个分支高度之和
    return getHeight(clust.left) + getHeight(clust.right)

# Description: 计算根节点总体误差
def getDepth(clust):
    # The distance of an endpoint（叶节点） is 0.0
    if clust.left == None and clust.right == None: return 0
    # The distance of a branch is the greater of its two sides plus its own distance
    return max(getDepth(clust.left), getDepth(clust.right)) + clust.distance

# Description: 为每一个最终生成的聚类创建一个高度为20pixel、宽度固定的图片
def drawDendrogram(clust, labels, jpeg='clusters.jpg'):
    # height and width
    h = getHeight(clust) * 20
    w = 1200
    depth = getDepth(clust)
    # width is fixed, so scale distances accordingly 缩放因子
    scaling = float(w - 150) / depth
    # Create a new image with a white background
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))
    # Draw the first node
    drawnode(draw, clust, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')

# Description: 绘制聚类节点，水平线条越短则两个聚类相似度很高
def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getHeight(clust.left) * 20
        h2 = getHeight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        # Line length
        ll = clust.distance * scaling
        # Vertical line from this cluster to children
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))
        # Horizontal line to left item
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))
        # Horizontal line to right item
        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0, 0))
        # Call the function to draw the left and right nodes
        drawnode(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
        drawnode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))

print('绘制聚类结果，保存到blogclust.jpg')
import os
if not os.path.isfile('blogclust.jpg'):
    print('图片不存在，将重新生成')
    drawDendrogram(clust, blogNames, jpeg='blogclust.jpg')
else: print('图片已存在')
print('****************************************************************************************')


# Description: 转置矩阵，用来进行列聚类
def rotateMatrix(data):
    newData=[]
    for i in range(len(data[0])):
        newRow=[ data[j][i] for j in range(len(data)) ]
        newData.append(newRow)
    return newData

print('数据集转置，单词成为行标签')
rotatedData=rotateMatrix(data)
print('按单词进行聚类（列聚类），由于单词数量比博客多很多，耗时很长')
# wordClust=hcluster(rotatedData)
if not os.path.isfile('wordclust.jpg'):
    print('图片不存在，将重新生成')
    # drawDendrogram(wordClust, labels=words, jpeg='wordclust.jpg')
else: print('图片已存在')
print('****************************************************************************************')


import random

# Description: K-均值聚类算法（k=4，默认迭代上限100次）
def kCluster(rows, distance=pearson, k=4):
    # 确定每个点的最小值和最大值
    ranges=[ (min([row[i] for row in rows]), max([row[i] for row in rows]))
             for i in range(len(rows[0])) ]
    # 随机创建k个中心点
    clusters=[ [random.random()*(ranges[i][1]-ranges[i][0]) + ranges[i][0]
                for i in range(len(rows[0]))]
               for j in range(k) ]
    lastMatches=None
    for t in range(100):
        print 'Iteration %d' % t
        bestMatches=[ [] for i in range(k) ]
        # 在每一行中寻找距离最近的中心点
        for j in range(len(rows)):
            row=rows[j]
            bestMatch=0
            for i in range(k):
                d=distance(clusters[i], row)
                if d<distance(clusters[bestMatch], row): bestMatch=i
            bestMatches[bestMatch].append(j)
        # 如果结果与上一次相同，则整个过程结束
        if bestMatches==lastMatches: break
        lastMatches=bestMatches
        # 把中心点移到其所有成员的平均位置处
        for i in range(k):
            avgs=[0.0]*len(rows[0])
            if len(bestMatches[i])>0:
                for rowId in bestMatches[i]:
                    for m in range(len(rows[rowId])):
                        avgs[m]+=rows[rowId][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestMatches[i])
                clusters[i]=avgs
    return bestMatches

print('博客数据聚类，k=10')
# kClusts=kCluster(data, k=10)
# for clust in kClusts:
#     print([blogNames[r] for r in clust])
print('****************************************************************************************')


# Description: 计算Tanimoto系数(相似度)
# Output: 0.0~1.0,1.0代表不存在同时喜欢两件物品的人，0.0代表所有人都同时喜欢两个向量中的物品
def tanimoto(v1, v2):
    c1, c2, share=0, 0, 0
    for i in range(len(v1)):
        if v1[i]!=0: c1+=1  # 出现在v1中
        if v2[i]!=0: c2+=1  # 出现在v2中
        if v1[i]!=0 and v2[i]!=0: share+=1  # 出现在两个向量中
    return 1.0 - (float(share) / (c1+c2-share))


print('对zebo数据进行聚类（分级聚类）')
wants, people, data = readfile('zebo.txt')
clust = hcluster(data, distance=tanimoto)
print('绘制聚类结果，保存到zebo.jpg')
if not os.path.isfile('zebo.jpg'):
    print('图片不存在，将重新生成')
    drawDendrogram(clust, wants, jpeg='zebo.jpg')
else: print('图片已存在')
print('****************************************************************************************')


# Description: 多维缩放（以二维形式展现数据），默认rate=0.01
# Output: 返回坐标的向量，即数据在二维图上的x,y坐标
def scaleDown(data, distance=pearson, rate=0.01):
    n=len(data)
    # 每一对数据项之间的真实距离
    realDist=[ [distance(data[i], data[j]) for j in range(n)] for i in range(n) ]
    # 随机初始化节点在二维空间中的起始位置
    loc=[ [random.random(), random.random()] for i in range(n) ]
    fakeDist=[ [0.0 for j in range(n)] for i in range(n) ]

    lastError=None
    for m in range(1000):
        # 寻找投影后的虚假距离
        for i in range(n):
            for j in range(n):
                fakeDist[i][j]=sqrt(sum( [pow(loc[i][x]-loc[j][x], 2)
                                          for x in range(len(loc[i]))] ))
        # 移动节点
        grad=[ [0.0, 0.0] for i in range(n) ]

        totalError=0
        for k in range(n):
            for j in range(n):
                if j==k: continue
                # 误差值=目标真实距离与当前虚假距离之间差值的百分比
                errorTerm=(fakeDist[j][k]-realDist[j][k]) / realDist[j][k]
                # 每一个节点根据误差，按比例偏移向其他节点
                grad[k][0]+=( (loc[k][0]-loc[j][0]) / fakeDist[j][k] ) * errorTerm
                grad[k][1]+=( (loc[k][1]-loc[j][1]) / fakeDist[j][k] ) * errorTerm
                # 记录总误差值
                totalError+=abs(errorTerm)
        print(totalError)
        # 如果节点移动后的情况更糟，则结束
        if lastError and lastError<totalError: break
        lastError=totalError
        # 根据rate与grad的乘积，移动每一个节点
        for k in range(n):
            loc[k][0]-=rate*grad[k][0]
            loc[k][1]-=rate*grad[k][1]
    return loc

# Description: 绘制二维图
def draw2d(data, labels, jpeg='multiDimScale2d.jpg'):
    img = Image.new('RGB', (2000, 2000), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0] + 0.5) * 1000
        y = (data[i][1] + 0.5) * 1000
        draw.text((x, y), labels[i], (0, 0, 0))
    img.save(jpeg, 'JPEG')

print('博客数据聚类（多维缩放），rate=0.01')
blogNames, words, data = readfile('blogdata.txt')
coords = scaleDown(data)
print('绘制聚类结果，保存到blogs2d.jpg')
if not os.path.isfile('blogs2d.jpg'):
    print('图片不存在，将重新生成')
    draw2d(coords, blogNames, jpeg='blogs2d.jpg')
else: print('图片已存在')
print('****************************************************************************************')






# -*- coding: utf-8 -*-

__author__ = 'DCLab'


# Description: 加载博客数据
def readfile(filename):
    lines=[line for line in file(filename)]
    # 第一行是列标题
    colnames=lines[0].strip().split('\t')[1:]
    rownames=[]
    data=[]
    for line in lines[1:]:
        p=line.strip().split('\t')
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
    sum1=sum(v1)
    sum2=sum(v2)
    # 求平方和
    sum1Sq=sum( [pow(v, 2) for v in v1] )
    sum2Sq=sum( [pow(v, 2) for v in v2] )
    # 求乘积之和
    pSum=sum( [v1[i]*v2[i] for i in range(len(v1))] )
    # 计算r
    numerator=pSum-(sum1*sum2/len(v1))
    denominator=sqrt( (sum1Sq-pow(sum1, 2)/len(v1))*(sum2Sq-pow(sum2, 2)/len(v1)) )
    if denominator==0: return 0
    r=numerator/denominator

    return 1.0-r

# 定义分级聚类中的聚类类型
class Bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.vec=vec
        self.left=left
        self.right=right
        self.distance=distance
        self.id=id


# Description: 分级聚类算法 TODO
def hcluster(rows, distance=pearson):
    distances={}
    currentClusterId=-1
    # 最开始的聚类就是数据集中的行
    clusts=[Bicluster(rows[i], id=i) for i in range(len(rows))]
    while len(clusts)>1:
        lowestPair=(0, 1)
        closest=distance(clusts[0].vec, clusts[1].vec)
        # 遍历每一个配对，寻找最小距离
        for i in range(len(clusts)):
            for j in range(i+1, len(clusts)):
                # 用distances缓存距离的计算值
                if (clusts[i].id, clusts[j].id) not in distances:
                    distances[(clusts[i].id, clusts[j].id)] = distance(clusts[i].vec, clusts[j].vec)
                d=distances[(clusts[i].id, clusts[j].id)]
                if d<closest:
                    closest=d
                    lowestPair=(i, j)
        # 计算两个聚类的均值
        mergeVec=[ (clusts[lowestPair[0]].vec[i] + clusts[lowestPair[1]].vec[i])/2.0
                   for i in range(len(clusts[0].vec)) ]
        # 建立新的聚类
        newCluster=Bicluster(mergeVec, left=clusts[lowestPair[0]], right=clusts[lowestPair[1]],
                             distance=closest, id=currentClusterId)
        # 不在原始集合中的聚类，其id为负数
        currentClusterId -= 1
        del clusts[lowestPair[1]]
        del clusts[lowestPair[0]]
        clusts.append(newCluster)

    return clusts[0]

print('分级聚类算法')
blogNames, words, data=readfile('blogdata.txt')
clust=hcluster(data)
print('****************************************************************************************')

# Description: 打印聚类结果 TODO
def printClusts(clust, labels=None, n=0):
    # 利用缩进来建立层级布局
    for i in range(n): print(' ')
    if clust.id<0:
        # 负数标记代表这是一个分支
        print('-')
    else:
        # 正数标记代表这是一个叶节点
        if labels==None: print(clust.id)
        else: print(labels[clust.id])
    # 打印右侧分支和左侧分支
    if clust.left!=None: printClusts(clust.left, labels=labels, n=n+1)
    if clust.right!=None: printClusts(clust.right, labels=labels, n=n+1)

print('打印聚类结果')
printClusts(clust, labels=blogNames)
print('****************************************************************************************')


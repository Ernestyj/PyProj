# -*- coding: utf-8 -*-

__author__ = 'DCLab'

import math

people=['Charlie','Augustus','Veruca','Violet','Mike','Joe','Willy','Miranda']

links=[('Augustus', 'Willy'),
       ('Mike', 'Joe'),
       ('Miranda', 'Mike'),
       ('Violet', 'Augustus'),
       ('Miranda', 'Willy'),
       ('Charlie', 'Mike'),
       ('Veruca', 'Joe'),
       ('Miranda', 'Augustus'),
       ('Willy', 'Augustus'),
       ('Joe', 'Charlie'),
       ('Veruca', 'Augustus'),
       ('Miranda', 'Joe')]

# Description: 连线交叉成本函数
def crosscount(v):
    # Convert the number list into a dictionary of person:(x,y)
    loc = dict([(people[i], (v[i * 2], v[i * 2 + 1])) for i in range(0, len(people))])
    total = 0
    # Loop through every pair of links
    for i in range(len(links)):
        for j in range(i + 1, len(links)):
            # Get the locations
            (x1, y1), (x2, y2) = loc[links[i][0]], loc[links[i][1]]
            (x3, y3), (x4, y4) = loc[links[j][0]], loc[links[j][1]]
            den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
            # den==0 if the lines are parallel
            if den == 0: continue
            # Otherwise ua and ub are the fraction of the
            # line where they cross
            ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
            ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den
            # If the fraction is between 0 and 1 for both lines then they cross each other
            if ua > 0 and ua < 1 and ub > 0 and ub < 1:
                total += 1
        for i in range(len(people)):
            for j in range(i + 1, len(people)):
                # Get the locations of the two nodes
                (x1, y1), (x2, y2) = loc[people[i]], loc[people[j]]
                # Find the distance between them
                dist = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
                # Penalize any nodes closer than 50 pixels
                if dist < 50:
                    total += (1.0 - (dist / 50.0))
    return total

# 假设将网络绘制于400*400图中，为了留出一定的页边，定义域可以稍小于该范围
domain = [(10, 370)] * (len(people) * 2)

from ex_optimization import randomoptimize, annealingoptimize

print('随机搜索连线交叉问题的最优题解，默认1000次猜测')
solution=randomoptimize(domain, crosscount)
print(crosscount(solution))
print(solution)
print('模拟退火算法搜索连线交叉问题的最优题解，T=10000.0, cool=0.99, step=50')
solution=annealingoptimize(domain, crosscount, step=50, cool=0.99)
print(crosscount(solution))
print(solution)
print('****************************************************************************************')


from PIL import Image, ImageDraw

# Description: 绘图
def drawnetwork(sol):
    # Create the image
    img = Image.new('RGB', (400, 400), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # Create the position dict
    pos = dict([(people[i], (sol[i * 2], sol[i * 2 + 1])) for i in range(0, len(people))])
    for (a, b) in links:
        draw.line((pos[a], pos[b]), fill=(255, 0, 0))
    for n, p in pos.items():
        draw.text(p, n, (0, 0, 0))
    img.show()

print('绘制网络图')
drawnetwork(solution)
print('****************************************************************************************')


import numpy as np
from minepy import MINE
import pandas as pd
import numpy.ma as ma
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="white", context="talk")


N = 23
SRA = (0.126, 0.097, 0.100, 0, 0.379, 0.221, 0.419, 0, 0.164, 0.272, 0.271, 0,
       0.199, 0.093, 0.212, 0, 0.314, 0.065, 0.084, 0, 0.023, 0.019, 0.158)
SVM = (0.126, 0.031, 0.410, 0, 0.281, 0.240, 0.208, 0, 0.188, 0.143, 0.271, 0,
       0.240, 0.093, 0.212, 0, 0.052, 0.106, 0.126, 0, 0.068, 0.057, 0.158)
RF = (0.126, 0.033, 0.100, 0, 0.127, 0.057, 0.106, 0, 0.267, 0.210, 0.198, 0,
       0.160, 0.120, 0.161, 0, 0.081, 0.107, 0.088, 0, 0.023, 0.019, 0.158)
SRA_A = (0.667, 0.455, 0.714, 0, 0.479, 0.485, 0.553, 0, 0.562, 0.500, 0.733, 0,
         0.857, 0.429, 0.833, 0, 0.558, 0.556, 0.500, 0, 0.857, 0.857, 0.750)
SVM_A = (0.667, 0.667, 0.714, 0, 0.447, 0.495, 0.500, 0, 0.625, 0.500, 0.733, 0,
         0.714, 0.429, 0.833, 0, 0.535, 0.478, 0.500, 0, 0.667, 0.333, 0.750)
m_SRA = ma.array(SRA)
for i in [3,7,11,15,19]: m_SRA[i] = ma.masked
m_SVM = ma.array(SVM)
for i in [3,7,11,15,19]: m_SVM[i] = ma.masked
m_RF = ma.array(RF)
for i in [3,7,11,15,19]: m_RF[i] = ma.masked
m_SRA_A = ma.array(SRA_A)
for i in [3,7,11,15,19]: m_SRA_A[i] = ma.masked
m_SVM_A = ma.array(SVM_A)
for i in [3,7,11,15,19]: m_SVM_A[i] = ma.masked

ind = np.arange(N)+1  # the x locations for the groups
width = 0.26       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, m_SRA, width, color='b')
rects2 = ax.bar(ind + width, m_SVM, width, color='g')
rects3 = ax.bar(ind + width*2, m_RF, width, color='y')
# rects1 = ax.plot(ind+0.3, m_SRA_A, 'g*-')
# rects2 = ax.plot(ind+0.3, m_SVM_A, 'y.--')

# add some text for labels, title and axes ticks
ax.set_ylabel('Annualized rate of return')
# ax.set_title('XXX')
ax.set_xticks(ind + width)
# ax.set_xticklabels(('D-300-2', 'D-016-2', 'D-905-2', 'W-300-2', 'W-016-2', 'W-905-2', 'M-300-2', 'M-016-2', 'M-905-2',
#                     'D-300-1', 'D-016-1', 'D-905-1', 'W-300-1', 'W-016-1', 'W-905-1', 'M-300-1', 'M-016-1', 'M-905-1'))
ax.set_xticklabels(('D-300-2', 'D-016-2', 'D-905-2', '', 'W-300-2', 'W-016-2', 'W-905-2', '', 'M-300-2', 'M-016-2', 'M-905-2', '',
                    'D-300-1', 'D-016-1', 'D-905-1', '', 'W-300-1', 'W-016-1', 'W-905-1', '', 'M-300-1', 'M-016-1', 'M-905-1'))


# ax1 = ax.twinx()
# line1 = ax1.plot(ax.get_xticks(), SRA_A, marker='o', color='g')
# line2 = ax1.plot(ax.get_xticks(), SVM_A, marker='^', color='y')

ax.legend((rects1[0], rects2[0], rects3[0]), ('SRAVoting', 'SVM', 'RF'))
# ax.legend((rects1[0], rects2[0], line1[0], line2[0]), ('SRAVoting', 'SVM', 'SRA_A', 'SVM_A'))

plt.xticks(rotation=90)
fig.subplots_adjust(bottom=0.15)
plt.show()
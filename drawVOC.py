"""
Created on 2022/11/20

@author: liupeng

"""

import os
import xml.etree.cElementTree as et
import matplotlib.pyplot as plt
from tqdm import tqdm

path = "/Users/liupeng/PycharmProjects/DataSet/VOCdevkit2007-gtsdb/VOC2007/Annotations"
# path = "/Users/liupeng/PycharmProjects/DataSet/VOCdevkit2007-ctsd/VOC2007/Annotations"
files = os.listdir(path)
plt.rcParams["axes.labelweight"] = "bold"  # 加粗

small = 32 * 32
medium = 96 * 96

smallArr_X = []
smallArr_Y = []
mediumArr_X = []
mediumArr_Y = []
largeArr_X = []
largeArr_Y = []
Axis_X_len = 140
Axis_Y_len = 140


def file_extension(path):
    return os.path.splitext(path)[1]


for xmlFile in tqdm(files, desc='Processing'):
    if not os.path.isdir(xmlFile):
        if file_extension(xmlFile) == '.xml':
            tree = et.parse(os.path.join(path, xmlFile))
            root = tree.getroot()
            filename = root.find('filename').text

            for Object in root.findall('object'):
                bndbox = Object.find('bndbox')
                xmin = bndbox.find('xmin').text
                ymin = bndbox.find('ymin').text
                xmax = bndbox.find('xmax').text
                ymax = bndbox.find('ymax').text

                # area = (int(ymax) - int(ymin)) * (int(xmax) - int(xmin))
                area = int(ymax) - int(ymin) if int(ymax) - int(ymin) > int(xmax) - int(xmin) else (
                        int(xmax) - int(xmin))
                if area <= small:
                    smallArr_X.append(int(xmax) - int(xmin))
                    smallArr_Y.append(int(ymax) - int(ymin))
                elif area > small and area <= medium:
                    mediumArr_X.append(int(xmax) - int(xmin))
                    mediumArr_Y.append(int(ymax) - int(ymin))
                else:
                    largeArr_X.append(int(xmax) - int(xmin))
                    largeArr_Y.append(int(ymax) - int(ymin))

fig, ax = plt.subplots()
smallType = ax.scatter(smallArr_X, smallArr_Y, marker='.', c='orange')
mediumType = ax.scatter(mediumArr_X, mediumArr_Y, marker='.', c='brown')
largeType = ax.scatter(largeArr_X, largeArr_Y, marker='.', c='darkblue')

# 浮窗
# plt.legend((smallType, mediumType, largeType), (
#    'small(%.0f%%' % (100 * round(len(smallArr_X) / (len(smallArr_X) + len(mediumArr_X) + len(largeArr_X)), 2)) + ')'
#    ,
#    'medium(%.0f%%' % (100 * round(len(mediumArr_X) / (len(smallArr_X) + len(mediumArr_X) + len(largeArr_X)), 2)) + ')'
#    ,
#   'large(%.0f%%' % (100 * round(len(largeArr_X) / (len(smallArr_X) + len(mediumArr_X) + len(largeArr_X)), 2)) + ')')
#           , loc='upper left', scatterpoints=1, labelspacing=1, edgecolor='black', framealpha=0.3, handletextpad=0)

plt.legend((smallType, mediumType, largeType), ('small', 'medium', 'large'), loc='upper left', scatterpoints=1,
           labelspacing=1, edgecolor='black', framealpha=0.3, handletextpad=0)

# plt.grid()
plt.xlim((0, Axis_X_len))
plt.ylim((0, Axis_Y_len))
plt.xlabel('Width')
plt.ylabel('Height')

ax1 = plt.gca()
ax1.patch.set_facecolor("snow")  # 设置 ax1 区域背景颜色
ax1.patch.set_alpha(0)  # 设置 ax1 区域背景颜色透明度

plt.show()

print('small(%.0f%%' % (100 * round(len(smallArr_X) / (len(smallArr_X) + len(mediumArr_X) + len(largeArr_X)), 2)) + ')')
print(
    'medium(%.0f%%' % (100 * round(len(mediumArr_X) / (len(smallArr_X) + len(mediumArr_X) + len(largeArr_X)), 2)) + ')')
print('large(%.0f%%' % (100 * round(len(largeArr_X) / (len(smallArr_X) + len(mediumArr_X) + len(largeArr_X)), 2)) + ')')

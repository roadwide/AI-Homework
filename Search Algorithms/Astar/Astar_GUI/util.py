import math
import random


# 将3x3矩阵转成3x3的文本
def matrix2text(matrix):
    text = ""
    for i in range(3):
        for j in range(3):
            text += str(matrix[i][j]) + " "
        text = text.rstrip(" ")    # 当前行结束时不需要空格
        text += "\n"
    text = text.rstrip("\n")    # 最后一行不需要换行
    return text


# 将一个元素为3x3矩阵的列表转成特定列的文本
def matrixList2text(matrixList, cols=8):
    if (len(matrixList) == 0): return ""
    rows = math.ceil(len(matrixList) / cols)
    text = ""
    for i in range(rows):    # 一行3x3矩阵
        for k in range(3):    # 一个3x3矩阵的3行
            curr_cols = cols if i+1 < rows else len(matrixList) - cols*i
            for j in range(curr_cols):    # 一行3x3矩阵中的一个
                idx = i * cols + j
                for l in range(3):    # 一个3x3矩阵的3列
                    text += str(matrixList[idx][k][l]) + " "
                text = text.rstrip(" ")
                text += "|"
            text = text.rstrip("|")
            text += "\n"
        text += "-"*curr_cols*6+"\n"
    text = text.rstrip("-"*curr_cols*6+"\n")
    return text


# 将矩阵转为一行显示，多行没法用treelib
def stat2TreeNode(stat):
    text = ""
    for i in range(3):
        for j in range(3):
            text += str(stat.stat[i][j]) + " "
    text += "F:{} G:{} H:{} NotInLoc:{}".format(stat.F, stat.G, stat.H, stat.NotInLoc)
    return text


#计算逆序数之和
def N(nums):
    N=0
    for i in range(len(nums)):
        if(nums[i]!=0):
            for j in range(i):
                if(nums[j]>nums[i]):
                    N+=1
    return N

#根据逆序数之和判断所给八数码是否可解
def judge(src,target):
    N1=N(src)
    N2=N(target)
    if(N1%2==N2%2):
        return True
    else:
        return False


# 返回一个可解的八数码矩阵
def getPuzzle():
    src = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    target = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    random.shuffle(src)
    while(not judge(src, target)):
        random.shuffle(src)
    matrix = []
    for i in range(3):
        matrix.append([])
        for j in range(3):
            matrix[-1].append(src[i*3+j])
    return matrix


#判断状态g是否在状态集合中，g是对象，gList是对象列表
#返回的结果是一个列表，第一个值是真假，如果是真则第二个值是g在gList中的位置索引
def isin(g,gList):
    gstat=g.stat
    statList=[]
    for i in gList:
        statList.append(i.stat)
    if(gstat in statList):
        res=[True,statList.index(gstat)]
    else:
        res=[False,0]
    return res
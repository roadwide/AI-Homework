import random
import math
import matplotlib.pyplot as plt
#读取数据
f=open("test.txt")
data=f.readlines()
#将cities初始化为字典，防止下面被当成列表
cities={}
for line in data:
    #原始数据以\n换行，将其替换掉
    line=line.replace("\n","")
    #最后一行以EOF为标志，如果读到就证明读完了，退出循环
    if(line=="EOF"):
        break
    #空格分割城市编号和城市的坐标
    city=line.split(" ")
    map(int,city)
    #将城市数据添加到cities中
    cities[eval(city[0])]=[eval(city[1]),eval(city[2])]
#计算适应度，也就是距离分之一，这里用伪欧氏距离
def calcfit(addr):
    sum=0
    for i in range(-1,len(addr)-1):
        nowcity=addr[i]
        nextcity=addr[i+1]
        nowloc=cities[nowcity]
        nextloc=cities[nextcity]
        sum+=math.sqrt(((nowloc[0]-nextloc[0])**2+(nowloc[1]-nextloc[1])**2)/10)
    #最后要回到初始城市
    return 1/sum

#生成交换序的函数，交换后数组b变为a，也就是a-b的结果
def switchB2A(a,b):
    #防止传进来的b被更改
    tmpb=b[:]
    q=[]
    for i in range(len(a)):
        if(a[i]!=tmpb[i]):
            j=b.index(a[i])
            q.append([i,j])
            #刚学的简洁的交换list的方法
            tmpb[j],tmpb[i]=tmpb[i],tmpb[j]
    return q

#w*v，w是一个数，v是一个数组。w乘v的数组长度，然后对结果取整，取数组的前这么多个元素
def multiply(w,v):
    l=int(w*len(v))
    res=v[0:l]
    return res

#鸟个体的类，实现鸟位置的移动
class Bird:
    def __init__(self,addr):
        self.addr=addr[:]
        self.v=0
        #初始化时自己曾遇到得最优位置就是初始化的位置
        # 经过尝试，发现在原代码中self.addr和self.bestAddr共同指向了addr，任一方的修改都会影响另一个变量(有时变好有时变差)，并且self.bestFit不会同步更新。因此在原代码中deltam始终为空集合，导致粒子的速度更新时从未考虑自己的最优值
        # 对init和upData中的代码进行了修改，添加[:]可避免self.addr和self.bestAddr共同访问同一存储空间的问题，加快收敛。
        self.bestAddr=addr[:]
        #初始状态没有速度
        self.v=[]
        self.fit=calcfit(addr)
        self.bestFit=calcfit(addr)

    #根据交换序移动位置
    def switch(self,switchq):
        for pair in switchq:
            i,j=pair[0],pair[1]
            self.addr[i],self.addr[j]=self.addr[j],self.addr[i]
        #交换后自动更行自己的成员变量
        self.upDate()

    #更新鸟自身相关信息
    def upDate(self):
        newfit=calcfit(self.addr)
        self.fit=newfit
        if(newfit>self.bestFit):
            self.bestFit=newfit
            self.bestAddr=self.addr[:]

    #变异操作
    #设置变异后避免了所有鸟都聚集到一个离食物近，但又不是最近的地方，并且就停在那里不动了
    def change(self):
        i,j=random.randrange(0,48),random.randrange(0,48)
        self.addr[i],self.addr[j]=self.addr[j],self.addr[i]
        self.upDate()
    #贪婪倒立变异
    def reverse(self):
        #随机选择一个城市
        cityx=random.randrange(1,49)
        noxcity=self.addr[:]
        noxcity.remove(cityx)
        maxFit=0
        nearCity=noxcity[0]
        for c in noxcity:
            fit=calcfit([c,cityx])
            if(fit>maxFit):
                maxFit=fit
                nearCity=c
        index1=self.addr.index(cityx)
        index2=self.addr.index(nearCity)
        tmp=self.addr[index1+1:index2+1]
        tmp.reverse()
        self.addr[index1+1:index2+1]=tmp
        self.upDate()

#种群的类，里面有很多鸟
class Group:
    def __init__(self):
        self.groupSize=500  #鸟的个数、粒子个数
        self.addrSize=48    #位置的维度，也就是TSP城市数量
        self.w=0.25 #w为惯性系数，也就是保留上次速度的程度
        self.pChange=0.1    #变异系数pChange
        self.pReverse=0.1   #贪婪倒立变异概率
        self.initBirds()
        self.best=self.getBest()
        self.Gen=0
    #初始化鸟群
    def initBirds(self):
        self.group=[]
        for i in range(self.groupSize):
            addr=[i+1 for i in range(self.addrSize)]
            random.shuffle(addr)
            bird=Bird(addr)
            self.group.append(bird)
    #获取当前离食物最近的鸟
    def getBest(self):
        bestFit=0
        bestBird=None
        #遍历群体里的所有鸟，找到路径最短的
        for bird in self.group:
            nowfit=calcfit(bird.addr)
            if(nowfit>bestFit):
                bestFit=nowfit
                bestBird=bird
        return bestBird
    #返回所有鸟的距离平均值
    def getAvg(self):
        sum=0
        for p in self.group:
            sum+=1/p.fit
        return sum/len(self.group)
    #打印最优位置的鸟的相关信息
    def showBest(self):
        print(self.Gen,":",1/self.best.fit)
    #更新每一只鸟的速度和位置
    def upDateBird(self):
        self.Gen+=1
        for bird in self.group:
            #g代表group，m代表me，分别代表自己和群组最优、自己最优的差
            deltag=switchB2A(self.best.addr,bird.addr)
            deltam=switchB2A(bird.bestAddr,bird.addr)
            newv=multiply(self.w,bird.v)[:]+multiply(random.random(),deltag)[:]+multiply(random.random(),deltam)
            bird.switch(newv)
            bird.v=newv
            if(random.random()<self.pChange):
                bird.change()
            if(random.random()<self.pReverse):
                bird.reverse()
            #顺便在循环里把最优的鸟更新了，防止二次遍历
            if(bird.fit>self.best.fit):
                self.best=bird

Gen=[]  #代数
dist=[] #距离
avgDist=[]  #平均距离
#上面三个列表是为了画图
group=Group()
i=0
#进行若干次迭代
while(i<500):
    i+=1
    group.upDateBird()
    group.showBest()
    Gen.append(i)
    dist.append(1/group.getBest().fit)
    avgDist.append(group.getAvg())
#将过程可视化
plt.plot(Gen,dist,'-r')
plt.plot(Gen,avgDist,'-b')
plt.show()


#下面是进行若干次重复实验的代码
# res=[]
# for p in range(1,11):
#     group=Group()
#     i=0
#     while(i<500):
#         i+=1
#         group.upDateBird()
#         #group.showBest()
#     res.append(1/group.getBest().fit)
#     print("第{}次实验\t当前最优{}".format(p,1/group.getBest().fit))
# sum=0
# for item in res:
#     sum+=item
# print("10次实验平均值",sum/len(res))

import math
import random
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
#用于决定释放多少信息素
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
#计算两个城市的距离，用于启发信息计算
def calc2c(c1,c2):
    #cities是一个字典，key是城市编号，value是一个两个元素的list，分别是x y的坐标
    return math.sqrt((cities[c1][0]-cities[c2][0])**2+(cities[c1][1]-cities[c2][1])**2)


#方便从1开始，所以0-48共49个数字
#全部初始化为1，否则后面的概率可能因为乘以0而全为0
#信息素浓度表
matrix=[[1 for i in range(49)] for i in range(49)]

#蚂蚁的类，实现了根据信息素和启发信息完成一次遍历
class Ant:
    def __init__(self):
        #tabu是已经走过的城市
        #规定从第一个城市开始走
        self.tabu=[1]
        self.allowed=[i for i in range(2,49)]
        self.nowCity=1
        #a,b分别表示信息素和期望启发因子的相对重要程度
        self.a=2
        self.b=7
        #rho表示路径上信息素的挥发系数，1-rho表示信息素的持久性系数。
        self.rho=0.1
        #本条路线的适应度，距离分之一
        self.fit=0
    #计算下一个城市去哪
    def next(self):
        sum=0
        #用一个数组储存下一个城市的概率
        p=[0 for i in range(49)]
        #计算分母和分子
        for c in self.allowed:
            tmp=math.pow(matrix[self.nowCity][c],self.a)*math.pow(1/calc2c(self.nowCity,c),self.b)
            sum+=tmp
            #此处p是分子
            p[c]=tmp
        #更新p为概率
        for c in self.allowed:
            p[c]=p[c]/sum
        #更新p为区间
        for i in range(1,49):
            p[i]+=p[i-1]
        r=random.random()
        for i in range(48):
            if(r<p[i+1] and r>p[i]):
                #i+1即为下一个要去的城市
                self.tabu.append(i+1)
                self.allowed.remove(i+1)
                self.nowCity=i+1
                return
    #将所有城市遍历
    def tour(self):
        while(self.allowed):
            self.next()
        self.fit=calcfit(self.tabu)


    #更新信息素矩阵
    def updateMatrix(self):
        #line储存本次经历过的城市
        line=[]
        for i in range(47):
            #因为矩阵是对阵的，2-1和1-2应该有相同的值，所以两个方向都要加
            line.append([self.tabu[i],self.tabu[i+1]])
            line.append([self.tabu[i+1],self.tabu[i]])
        for i in range(1,49):
            for j in range(1,49):
                if([i,j] in line):
                    matrix[i][j]=(1-self.rho)*matrix[i][j]+self.fit
                else:
                    matrix[i][j]=(1-self.rho)*matrix[i][j]
    #一只蚂蚁复用，每次恢复初始状态
    def clear(self):
        self.tabu=[1]
        self.allowed=[i for i in range(2,49)]
        self.nowCity=1
        self.fit=0


#蚁群算法的类，实现了算法运行过程
class ACO:
    def __init__(self):
        #初始先随机N只蚂蚁
        self.initN=200
        self.bestTour=[i for i in range(1,49)]
        self.bestFit=calcfit(self.bestTour)
        self.initAnt()

    def initAnt(self):
        i=0
        tmpAnt=Ant()
        print(self.initN,"只先锋蚂蚁正在探路")
        while(i<self.initN):
            i+=1
            tmpTour=[i for i in range(1,49)]
            random.shuffle(tmpTour)
            tmpAnt.tabu=tmpTour
            tmpAnt.allowed=[]
            tmpAnt.updateMatrix()
            tmpFit=calcfit(tmpAnt.tabu)
            if(tmpFit>self.bestFit):
                self.bestFit=tmpFit
                self.bestTour=tmpAnt.tabu
            tmpAnt.clear()

    #n为蚂蚁数量
    def startAnt(self,n):
        i=0
        ant=Ant()
        Gen=[]  #迭代次数
        dist=[] #距离，这两个列表是为了画图
        while(i<n):
            i+=1
            ant.tour()
            if(ant.fit>self.bestFit):
                self.bestFit=ant.fit
                self.bestTour=ant.tabu
            print(i,":",1/self.bestFit)
            ant.clear()
            Gen.append(i)
            dist.append(1/self.bestFit)
        #绘制求解过程曲线
        plt.plot(Gen,dist,'-r')
        plt.show()


a=ACO()
a.startAnt(1000)

#下面是若干次重复实验测试的代码
# res=[]
# for i in range(1,11):
#     a=ACO()
#     a.startAnt(1000)
#     res.append(1/a.bestFit)
#     print("第{}次实验\t当前最优解{}".format(i,1/a.bestFit))
# sum=0
# for item in res:
#     sum+=item
# print("10次实验平均解",sum/len(res))

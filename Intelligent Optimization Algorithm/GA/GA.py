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
def calcfit(gene):
    sum=0
    #最后要回到初始城市所以从-1，也就是最后一个城市绕一圈到最后一个城市
    for i in range(-1,len(gene)-1):
        nowcity=gene[i]
        nextcity=gene[i+1]
        nowloc=cities[nowcity]
        nextloc=cities[nextcity]
        sum+=math.sqrt(((nowloc[0]-nextloc[0])**2+(nowloc[1]-nextloc[1])**2)/10)

    return 1/sum

#每个个体的类，方便根据基因计算适应度
class Person:
    def __init__(self,gene):
        self.gene=gene
        self.fit=calcfit(gene)
class Group:
    def __init__(self):
        self.GroupSize=100  #种群规模
        self.GeneSize=48    #基因数量，也就是城市数量
        self.initGroup()
        self.upDate()
    #初始化种群，随机生成若干个体
    def initGroup(self):
        self.group=[]
        i=0
        while(i<self.GroupSize):
            i+=1
            #gene如果在for以外生成只会shuffle一次
            gene=[i+1 for i in range(self.GeneSize)]
            random.shuffle(gene)
            tmpPerson=Person(gene)
            self.group.append(tmpPerson)

    #获取种群中适应度最高的个体
    def getBest(self):
        bestFit=self.group[0].fit
        best=self.group[0]
        for person in self.group:
            if(person.fit>bestFit):
                bestFit=person.fit
                best=person
        return best
    #计算种群中所有个体的平均距离
    def getAvg(self):
        sum=0
        for p in self.group:
            sum+=1/p.fit
        return sum/len(self.group)
    #根据适应度，使用轮盘赌返回一个个体，用于遗传交叉
    def getOne(self):
        #section的简称，区间
        sec=[0]
        sumsec=0
        for person in self.group:
            sumsec+=person.fit
            sec.append(sumsec)
        p=random.random()*sumsec
        for i in range(len(sec)):
            if(p>sec[i] and p<sec[i+1]):
                #这里注意区间是比个体多一个0的
                return self.group[i]
    #更新种群相关信息
    def upDate(self):
        self.best=self.getBest()
#遗传算法的类，定义了遗传、交叉、变异等操作
class GA:
    def __init__(self):
        self.group=Group()
        self.pCross=0.35    #交叉率
        self.pChange=0.1    #变异率
        self.Gen=1  #代数

    #变异操作
    def change(self,gene):
        #把列表随机的一段取出然后再随机插入某个位置
        #length是取出基因的长度，postake是取出的位置，posins是插入的位置
        geneLenght=len(gene)
        index1 = random.randint(0, geneLenght - 1)
        index2 = random.randint(0, geneLenght - 1)
        newGene = gene[:]       # 产生一个新的基因序列，以免变异的时候影响父种群
        newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
        return newGene

    #交叉操作
    def cross(self,p1,p2):
        geneLenght=len(p1.gene)
        index1 = random.randint(0, geneLenght - 1)
        index2 = random.randint(index1, geneLenght - 1)
        tempGene = p2.gene[index1:index2]   # 交叉的基因片段
        newGene = []
        p1len = 0
        for g in p1.gene:
              if p1len == index1:
                    newGene.extend(tempGene)     # 插入基因片段
                    p1len += 1
              if g not in tempGene:
                    newGene.append(g)
                    p1len += 1
        return newGene

    #获取下一代
    def nextGen(self):
        self.Gen+=1
        #nextGen代表下一代的所有基因
        nextGen=[]
        #将最优秀的基因直接传递给下一代
        nextGen.append(self.group.getBest().gene[:])
        while(len(nextGen)<self.group.GroupSize):
            pChange=random.random()
            pCross=random.random()
            p1=self.group.getOne()
            if(pCross<self.pCross):
                p2=self.group.getOne()
                newGene=self.cross(p1,p2)
            else:
                newGene=p1.gene[:]
            if(pChange<self.pChange):
                newGene=self.change(newGene)
            nextGen.append(newGene)
        self.group.group=[]
        for gene in nextGen:
            self.group.group.append(Person(gene))
            self.group.upDate()

    #打印当前种群的最优个体信息
    def showBest(self):
        print("第{}代\t当前最优{}\t当前平均{}\t".format(self.Gen,1/self.group.getBest().fit,self.group.getAvg()))

    #n代表代数，遗传算法的入口
    def run(self,n):
        Gen=[]  #代数
        dist=[] #每一代的最优距离
        avgDist=[]  #每一代的平均距离
        #上面三个列表是为了画图
        i=1
        while(i<n):
            self.nextGen()
            self.showBest()
            i+=1
            Gen.append(i)
            dist.append(1/self.group.getBest().fit)
            avgDist.append(self.group.getAvg())
        #绘制进化曲线
        plt.plot(Gen,dist,'-r')
        plt.plot(Gen,avgDist,'-b')
        plt.show()

ga=GA()
ga.run(3000)
print("进行3000代后最优解：",1/ga.group.getBest().fit)

#下面是进行若干次重复实验的代码
# res=[]
# for i in range(1,11):
#     ga=GA()
#     ga.run(3000)
#     print("第{}次实验最优解{}".format(i,1/ga.group.getBest().fit))
#     res.append(1/ga.group.getBest().fit)
# sum=0
# for item in res:
#     sum+=item
# print("10次实验的平均距离",sum/len(res))

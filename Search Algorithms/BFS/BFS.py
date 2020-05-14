import copy
#棋盘的类，实现移动和扩展状态
class grid:
    def __init__(self,stat):
        self.pre=None
        self.target=[[1,2,3],[8,0,4],[7,6,5]]
        self.stat=stat
        self.find0()
        self.update()
    #更新深度和距离和
    def update(self):
        self.fH()
        self.fG()
    #G是深度，也就是走的步数
    def fG(self):
        if(self.pre!=None):
            self.G=self.pre.G+1
        else:
            self.G=0
    #H是和目标状态距离之和，可以用来判断是否达到最优解
    def fH(self):
        self.H=0
        for i in range(3):
            for j in range(3):
                targetX=self.target[i][j]
                nowP=self.findx(targetX)
                self.H+=abs(nowP[0]-i)+abs(nowP[1]-j)
    #查看当前状态
    def see(self):
        print("depth：",self.G)
        for i in range(3):
             print(self.stat[i])
        print("-"*10)
    #查看找到的解是如何从头移动的
    def seeAns(self):
        ans=[]
        ans.append(self)
        p=self.pre
        while(p):
            ans.append(p)
            p=p.pre
        ans.reverse()
        for i in ans:
            i.see()
    #找到数字x的位置，返回其坐标
    def findx(self,x):
        for i in range(3):
            if(x in self.stat[i]):
                j=self.stat[i].index(x)
                return [i,j]
    #找到0，也就是空白格的位置
    def find0(self):
            self.zero=self.findx(0)
    #对当前状态进行所有可能的扩展，返回一个扩展状态的列表
    def expand(self):
        i=self.zero[0]
        j=self.zero[1]
        gridList=[]

        if(j==2 or j==1):
            gridList.append(self.left())
        if(i==2 or i==1):
            gridList.append(self.up())
        if(i==0 or i==1):
            gridList.append(self.down())
        if(j==0 or j==1):
            gridList.append(self.right())

        return gridList


    #deepcopy多维列表的复制，防止指针赋值将原列表改变
    #move只能移动行或列，即row和col必有一个为0
    #对当前状态进行移动
    def move(self,row,col):
        newStat=copy.deepcopy(self.stat)
        tmp=self.stat[self.zero[0]+row][self.zero[1]+col]
        newStat[self.zero[0]][self.zero[1]]=tmp
        newStat[self.zero[0]+row][self.zero[1]+col]=0
        return newStat

    def up(self):
        return self.move(-1,0)

    def down(self):
        return self.move(1,0)

    def left(self):
        return self.move(0,-1)

    def right(self):
        return self.move(0,1)


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

#初始化状态
startStat=[[2,8,3],[1,0,4],[7,6,5]]
g=grid(startStat)
if(judge(startStat,g.target)!=True):
    print("所给八数码无解，请检查输入")
    exit(1)

visited=[]
queue=[g]
time=0
while(queue):
    time+=1
    v=queue.pop(0)
    #判断是否找到解
    if(v.H==0):
        print("found and times:",time,"moves:",v.G)
        #查看找到的解是如何从头移动的
        v.seeAns()
        break
    else:
        #对当前状态进行扩展
        visited.append(v.stat)
        expandStats=v.expand()
        for stat in expandStats:
            tmpG=grid(stat)
            tmpG.pre=v
            tmpG.update()
            if(stat not in visited):
                queue.append(tmpG)

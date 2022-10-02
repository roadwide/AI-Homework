import copy
#棋盘的类，实现移动和扩展状态
class grid:
    def __init__(self,stat, heuristic_method):
        # heuristic_method
        # 0 深度+曼哈顿距离
        # 1 曼哈顿距离
        # 2 不在位置方块数
        self.heuristic_method = heuristic_method

        self.pre=None
        #stat是一个二维列表
        self.stat=stat
        self.find0()
        self.update()

    #更新启发函数的相关信息
    def update(self):
        self.fH()
        self.fG()
        self.countNotInLoc()
        self.fF()

    #G是深度，也就是走的步数
    def fG(self):
        if(self.pre!=None):
            self.G=self.pre.G+1
        else:
            self.G=0

    #H是和目标状态距离之和
    def fH(self):
        target=[[1,2,3],[4,5,6],[7,8,0]]
        self.H=0
        for i in range(3):
            for j in range(3):
                targetX=target[i][j]
                nowP=self.findx(targetX)
                #曼哈顿距离之和
                self.H+=abs(nowP[0]-i)+abs(nowP[1]-j)
    
    # 统计不在位置的方块数
    def countNotInLoc(self):
        target=[[1,2,3],[4,5,6],[7,8,0]]
        self.NotInLoc = 0
        for i in range(3):
            for j in range(3):
                targetX=target[i][j]
                nowP=self.findx(targetX)
                #曼哈顿距离之和
                if(abs(nowP[0]-i)+abs(nowP[1]-j)!=0):
                    self.NotInLoc += 1


    #F是启发函数，F=G+H
    def fF(self):
        if(self.heuristic_method == 0):
            self.F=self.G+self.H
        elif(self.heuristic_method == 1):
            self.F=self.H
        elif(self.heuristic_method == 2):
            self.F=self.NotInLoc

    #以三行三列的形式输出当前状态
    def see(self):
        for i in range(3):
             print(self.stat[i])
        print("F=",self.F,"G=",self.G,"H=",self.H)
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

    #找到数字x的位置
    def findx(self,x):
        for i in range(3):
            if(x in self.stat[i]):
                j=self.stat[i].index(x)
                return [i,j]

    #找到0，也就是空白格的位置
    def find0(self):
        self.zero=self.findx(0)

    #扩展当前状态，也就是上下左右移动。返回的是一个状态列表，也就是包含stat的列表
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
    #向某个方向移动
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
import time
import tkinter as tk
import tkinter.messagebox
from util import *
from grid import grid
from treelib import Tree

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("eight puzzle")
        self.master.geometry('780x600+100+100')
        self.grid()
        self.heuristic_method = 0
        self.create_widgets()
        self.set_init_puzzle()
        self.expandStats = []
        

    def create_widgets(self):
        self.init_stat = tk.Label(self, text="\n\n", padx=10)
        self.init_stat.grid(column=0, row=0)
        self.curr_min_stat = tk.Label(self, padx=10)
        self.curr_min_stat.grid(column=1, row=0)
        self.curr_expand_stat = tk.Label(self, padx=10)
        self.curr_expand_stat.grid(column=2, row=0)
        self.title1 = tk.Label(self, text="初始状态", padx=10)
        self.title1.grid(column=0, row=1)
        self.title2 = tk.Label(self, text="open表中最小", padx=10)
        self.title2.grid(column=1, row=1)
        self.title3 = tk.Label(self, text="当前扩展状态", padx=10)
        self.title3.grid(column=2, row=1)

        self.select_function_tip = tk.Label(self, text="选择启发函数>>>")
        self.select_function_tip.grid(column=0, row=2)
        self.heuristic_function_list = tk.Listbox(self, height=3)
        self.heuristic_function_list.grid(column=1, row=2, columnspan=2, pady=10)
        for i,item in enumerate(["深度+曼哈顿距离", "曼哈顿距离", "不在位置方块数"]):
            self.heuristic_function_list.insert(i,item)
        self.heuristic_function_list.bind('<<ListboxSelect>>', self.listbox_click)
        self.heuristic_function_list.select_set(0)    # 默认选择第一项

        self.init_button = tk.Button(self, text="随机初始化", command=self.set_init_puzzle)
        self.init_button.grid(column=0, row=3)
        self.one_step_button = tk.Button(self, text="单步执行", command=self.next_step)
        self.one_step_button.grid(column=1, row=3)
        self.continus_step_button = tk.Button(self, text="连续执行", command=self.all_step)
        self.continus_step_button.grid(column=2, row=3)
        # self.draw_search_tree_button = tk.Button(self, text="绘制搜索树")
        # self.draw_search_tree_button.grid(column=0, row=4)
        self.expand_num_button = tk.Button(self, text="统计扩展节点数", command=self.show_expand_num)
        self.expand_num_button.grid(column=1, row=4)
        self.show_exec_time_button = tk.Button(self, text="显示执行时间", command=self.show_exec_time)
        self.show_exec_time_button.grid(column=2, row=4)

        self.open_show_tip = tk.Label(self, text="open表实时显示")
        self.open_show_tip.grid(column=0, row=5, pady=10)
        self.open_list_text = tk.Text(self, width=50, height=10, state=tk.DISABLED)
        self.open_list_text.grid(column=0, row=6, columnspan=3)

        self.closed_show_tip = tk.Label(self, text="closed表实时显示")
        self.closed_show_tip.grid(column=0, row=7, pady=10)
        self.closed_list_text = tk.Text(self, width=50, height=10, state=tk.DISABLED)
        self.closed_list_text.grid(column=0, row=8, columnspan=3)

        self.tree_show_tip = tk.Label(self, text="搜索树实时显示")
        self.tree_show_tip.grid(column=4, row=0)
        self.tree_text = tk.Text(self, width=55, height=40, state=tk.DISABLED, wrap="none")
        self.tree_text.grid(column=4, row=1, rowspan=8, padx=20)


    def set_init_stat(self, text):
        self.init_stat["text"] = text
    

    def set_curr_min_stat(self, text):
        self.curr_min_stat["text"] = text
    

    def set_curr_expand_stat(self, text):
        self.curr_expand_stat["text"] = text


    def show_expand_num(self):
        tkinter.messagebox.showinfo(title="结果", message="扩展节点数: {}".format(len(self.open)+len(self.closed)))
    

    def show_exec_time(self):
        tkinter.messagebox.showinfo(title="结果", message="算法执行时间: {}".format(self.step_time))
        

    def set_open_text(self, text):
        self.open_list_text.config(state=tk.NORMAL)
        self.open_list_text.delete(1.0, tk.END) 
        self.open_list_text.insert(tk.END, text)
        self.open_list_text.config(state=tk.DISABLED)


    def set_closed_text(self, text):
        self.closed_list_text.config(state=tk.NORMAL)
        self.closed_list_text.delete(1.0, tk.END)
        self.closed_list_text.insert(tk.END, text)
        self.closed_list_text.config(state=tk.DISABLED)

    def set_tree_text(self, text):
        self.tree_text.config(state=tk.NORMAL)
        self.tree_text.delete(1.0, tk.END)
        self.tree_text.insert(tk.END, text)
        self.tree_text.config(state=tk.DISABLED)
    
    def set_init_puzzle(self, puzzle=None):
        self.node = []
        self.tree = Tree()
        self.puzzle_matrix = puzzle if puzzle else getPuzzle()
        g = grid(self.puzzle_matrix, self.heuristic_method)
        self.insert_node(g)
        self.open = [g]    # 防止非空
        self.closed = []
        puzzle_text = matrix2text(self.puzzle_matrix)
        self.init_stat["text"] = puzzle_text
        self.curr_min_stat["text"] = ""
        self.curr_expand_stat["text"] = ""
        self.step_time = 0
        self.update_open_text()
        self.update_closed_text()
    
    def insert_node(self, node):
        # node 是一个grid实例
        if (node not in self.node):
            self.node.append(node)
            if (node.pre == None):    # 根节点
                self.tree.create_node(stat2TreeNode(node), self.node.index(node))
            else:
                self.tree.create_node(stat2TreeNode(node), self.node.index(node), self.node.index(node.pre))
        self.set_tree_text(self.tree.show(stdout=False))

    

    def update_open_text(self):
        openList = []
        for g in self.open:
            openList.append(g.stat)
        text = matrixList2text(openList)
        self.set_open_text(text)
    
    def update_closed_text(self):
        closedList = []
        for g in self.closed:
            closedList.append(g.stat)
        text = matrixList2text(closedList)
        self.set_closed_text(text)


    # 启发函数选择列表被点击时触发事件    
    def listbox_click(self, event):    # 要传event，具体原因不详
        try:
            # 更换启发式函数
            self.heuristic_method=self.heuristic_function_list.curselection()[0]
            self.set_init_puzzle(self.puzzle_matrix)    # 更换启发式函数后重置，但初始矩阵不变
        except:
            pass    # 失去焦点

    
    def next_step(self):
        self.step_time += 1
        if (len(self.expandStats) == 0):
            #根据启发函数值对open进行排序，默认升序
            self.open.sort(key=lambda G:G.F)
            #找出启发函数值最小的进行扩展
            self.minFStat=self.open[0]
            self.curr_min_stat["text"] = matrix2text(self.minFStat.stat)
            #检查是否找到解，如果找到则从头输出移动步骤
            if(self.minFStat.H==0):
                tkinter.messagebox.showinfo(title="结果", message="扩展节点数: {}\n算法执行时间: {}".format(len(self.open)+len(self.closed), self.step_time))
                self.minFStat.seeAns()
                return
            #走到这里证明还没有找到解，对启发函数值最小的进行扩展
            self.open.pop(0)
            self.update_open_text()
            self.closed.append(self.minFStat)
            self.update_closed_text()
            self.expandStats=self.minFStat.expand()
        else:
            statMatrix = self.expandStats.pop()
            self.curr_expand_stat["text"] = matrix2text(statMatrix)
            #将扩展出来的状态（二维列表）实例化为grid对象
            tmpG=grid(statMatrix, self.heuristic_method)
            #指针指向父节点
            tmpG.pre=self.minFStat
            #初始化时没有pre，所以G初始化时都是0
            #在设置pre之后应该更新G和F
            tmpG.update()
            self.insert_node(tmpG)
            #查看扩展出的状态是否已经存在与open或closed中
            findstat=isin(tmpG,self.open)
            findstat2=isin(tmpG,self.closed)
            #在closed中,判断是否更新
            if(findstat2[0]==True and tmpG.F<self.closed[findstat2[1]].F):
                self.closed[findstat2[1]]=tmpG
                self.open.append(tmpG)
                self.update_open_text()
            #在open中，判断是否更新
            if(findstat[0]==True and tmpG.F<self.open[findstat[1]].F):
                self.open[findstat[1]]=tmpG
            #tmpG状态不在open中，也不在closed中
            if(findstat[0]==False and findstat2[0]==False):
                self.open.append(tmpG)
                self.update_open_text()

    def all_step(self):
        self.next_step()    # 防止一开始就连续执行导致下面的while self.minFStat不存在
        while(self.minFStat.H!=0):
            self.next_step()
            self.update()
    
            

if __name__ == "__main__":

    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
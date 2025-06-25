import random
import numpy as np
from scipy.optimize import minimize
import math
import matplotlib.pyplot as plt

class f:  # 拟合点生成函数
    def __init__(self, sigma):
        self.a = random.randint(1, 5)
        self.b = random.randint(1, 10)
        self.sigma = sigma
        print("拟合点生成函数为：y=%dx+%d+ω，ω~N(0,%d)" % (self.a, self.b, (self.sigma) ** 2))

    def y(self, x):
        omega = random.gauss(0, self.sigma)
        y = self.a * x + self.b + omega
        return y

def loss(a_list):  # 定义损失函数
    g_list = np.dot(X_part, a_list)
    I=g_list-y_list
    sum=0
    for i in I:
        sum+=abs(i)
    return sum

while 1:
    # 生成拟合函数
    while 1:
        try:
            sigma = int(input("输入符合正态分布的白噪音ω~N(0,δ)中δ的取值："))
            break
        except:
            print("非法输入，请重新输入！")
            continue
    f1 = f(sigma)
    # 生成拟合点
    x_list = np.random.rand(20) * 10
    x_list = sorted(x_list)
    print("拟合点横坐标为：", x_list)
    y_list = []
    for x in x_list:
        y_list.append(f1.y(x))
    print("拟合点对应纵坐标为：", y_list)
    # 建立自变量矩阵
    X = np.zeros([20, 11])
    for i in range(20):
        x = x_list[i]
        for j in range(11):
            X[i, j] = math.pow(x, 10-j)
    #print(X)  #X行向量依次为xi^n,xi^(n-1),...,xi^0，x1第一行x2第二行直至xn以此类推
    # 逼近
    for i in range(1, 11):
        print("\n***************%d次多项式拟合***************" % i)
        a_list = np.zeros((1, i + 1)).T  # a_list为待优化的多项式系数组成的行向量，依次为ai,a(i-1),...,a0
        X_part = X[...,10-i:]
        Var=20*pow(math.ceil(sigma),1.5)    #通过修改Var的计算公式可改变拟合的精度，但追求拟合的精度可能导致程序运行效率低下
        ii=0
        while 1:    #循环优化过程使损失函数值在目标Var以下，或者循环到一定程度退出
            res=minimize(loss, a_list,method='nelder-mead',options={'xatol': 1e-8, 'disp': False})
            a_list=res.x
            ii+=1
            if res.fun>Var and ii<=15:
                continue
            else: break
        poly=np.poly1d(res.x)
        print('%d次多项式为：\n'%i,poly)
        print('%d次多项式拟合的损失函数距离为:' % i,res.fun)
        # 作图
        x=np.linspace(0, 10, 1000)
        plt.scatter(x_list,y_list)
        plt.plot(x,np.polyval(poly, x))
        plt.title('regression: %d degree polynomial'%i)
        plt.show()
    Var = input("输入N或n结束程序，其他任意键进行新拟合：")
    if Var == 'N' or Var == "n":
        break
# encoding:utf8
import numpy as np

'''
输入一个多项分布的向量p，生成一个该多项分布的样本列表
'''

'''
mcmc
MCMC采样算法,求一个随机变量的样本列表，提供这个随机变量多项分布的参数
p:	numpy.float32向量，各元素相加<=1,且各元素>=0
	多项分布的概率分布，或者一个已知分布的概率密度
leninitstate:	整数>1，给的初始状态个样本长度,得到的多项分布的样本个数
convergelimit：	整数，连续convergelimit+1次采样不发生变化认为过程收敛
ismh:	bool值，是否使用MH算法，若否，使用最原始的MC算法
return:	整数列表，长度为leninitstate的样本列表，每个值代表此随机变量的状态
		符合p分布的一个样本
'''


def mcmc(p=np.array([.1, .2, .3, .4]), leninitstate=4, convergelimit=10, ismh=True):
    # 验证p的类型和条件
    # 生成一个转移矩阵
    A = np.array([[1.0 / len(p) for x in range(len(p))]
                  for y in range(len(p))], dtype=np.float32)
    # 初始状态
    initstate = [np.random.randint(len(p)) for x in range(leninitstate)]
    # 初始收敛计数
    convergenum = 0
    # 采样计数
    samplecount = 0
    while True:
        # 选择一个要更改的样本index
        index = np.random.randint(leninitstate)
        # 按照当前状态和状态转移矩阵A 采样一个新的状态
        cur = np.argmax(np.random.multinomial(1, A[initstate[index]]))
        samplecount += 1
        # 计算接收率 A[j][i]*p[j]
        alpha = 0
        if ismh:
            alpha = min(
                [1, (A[cur][initstate[index]] * p[cur]) / (A[initstate[index]][cur] * p[initstate[index]])])
        else:
            alpha = A[cur][initstate[index]] * p[cur]
        if np.random.ranf() < alpha:
            print '采样到:' + str(cur) + ' === 此次采样前状态未变更次数：' + str(convergenum * '#')
            if cur == initstate[index]:
                # 状态未变更
                if convergenum >= convergelimit:
                    # 状态连续多次未变更，收敛返回
                    print '收敛状态：' + str(initstate)
                    print '采样计数：' + str(samplecount)
                    return initstate
                else:
                    # 状态未变更但还不稳定，稳定计数增加
                    convergenum += 1
            else:
                # 有状态变更，修改
                initstate[index] = cur
                convergenum = 0


mcmc(ismh=True, leninitstate=10)
raw_input('press any key to continue...')

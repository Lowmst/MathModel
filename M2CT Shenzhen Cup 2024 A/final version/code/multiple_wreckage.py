from utils import *

import numpy as np
import scipy.optimize as opt



def solve(locs, times):

    # 取音速为0.34km/s
    v = 0.34

    # 计算各监测设备之间的距离
    dists = np.zeros((7, 7))
    for dev_idx_1 in range(6):
        for dev_idx_2 in range(dev_idx_1 + 1, 7):
            dists[dev_idx_1, dev_idx_2] = distance(locs[dev_idx_1], locs[dev_idx_2])
            dists[dev_idx_2, dev_idx_1] = dists[dev_idx_1, dev_idx_2]

    # 维护7*4个布尔矩阵，表示times中某时间数据相对于其余数据是否应被选取为同一组
    selected = [[np.full_like(times, True, dtype=bool) for i in range(4)] for j in range(7)]
    for dev_idx_1 in range(7):
        for time_idx_1 in range(4):
            for dev_idx_2 in range(7):
                for time_idx_2 in range(4):
                    selected[dev_idx_1][time_idx_1][dev_idx_2, time_idx_2] = (abs(times[dev_idx_1, time_idx_1] - times[dev_idx_2, time_idx_2]) <= (dists[dev_idx_1, dev_idx_2])/v)


    # 最终选取的4组时间数据，初始化为List
    anss = []

    # 以设备A的4个时间数据为参照，设置4个循环得到4组最终数据
    for main_idx in range(4):
        tmp_anss = []
        tmp_ans = []

        def dfs(dev_idx):
            if dev_idx == 7:
                tmp_anss.append(list(tmp_ans))
                return
            for time_idx in range(4):
                if (not check_selected(dev_idx, time_idx)) or (not check_ans(dev_idx, time_idx)):
                    continue
                tmp_ans.append(time_idx)
                dfs(dev_idx + 1)
                tmp_ans.pop() # 去除栈中最后一位

        def check_selected(dev_idx, time_idx):
            for i in range(len(tmp_ans)):
                if not selected[dev_idx][time_idx][i, tmp_ans[i]]:
                    return False
            return True

        def check_ans(dev_idx, time_idx):
            for ans in anss:
                try:
                    if time_idx == ans[dev_idx]:
                        return False
                except:
                    return True
            return True

        tmp_ans.append(main_idx)
        dfs(1)


        tmp_anss_x = []
        tmp_anss_fun = []

        for tmp_ans in tmp_anss:
            time = [times[dev_idx, tmp_ans[dev_idx]] for dev_idx in range(len(tmp_ans))]

            @np.vectorize(excluded=[0])
            def f(x, i):
                return distance(locs[i, :], x[0:3]) - (time[i] - x[3]) * v

            def s(x):
                return np.sum(f(x, [0,1,2,3,4,5,6])**2)

            constraint = [{'type': 'ineq', 'fun': lambda x: x[2]}]
            result = opt.minimize(s, [0, 0, 12, 0], constraints=constraint)
            # result = opt.dual_annealing(s, bounds=[[0,200],[0,200],[0,15],[-50,70]])

            tmp_anss_x.append(result.x)
            tmp_anss_fun.append(result.fun)
            # result = opt.basinhopping(s, [48,0,12,0])

        ans_idx = tmp_anss_fun.index(min(tmp_anss_fun))


        return_val = tmp_anss[ans_idx]
        return_val.append(tmp_anss_x[ans_idx])
        return_val.append(tmp_anss_fun[ans_idx])
        anss.append(return_val)

    return anss



# 原始数据输入
data = np.array(
    [
        [110.241, 27.204, 824, 100.767, 164.229, 214.850, 270.065],
        [110.783, 27.456, 727, 92.453, 112.220, 169.362, 196.583],
        [110.762, 27.785, 742, 75.560, 110.696, 156.936, 188.020],
        [110.251, 28.025, 850, 94.653, 141.409, 196.517, 258.985],
        [110.524, 27.617, 786, 78.600, 86.216, 118.443, 126.669],
        [110.467, 28.081, 678, 67.274, 166.270, 175.482, 266.871],
        [110.047, 27.521, 575, 103.738, 163.024, 206.789, 210.306]
    ]
)

# 取转换为空间直角坐标系的监测设备坐标
locs = convert(data[:, 0:3], 'xyz')

# 取各监测设备接收的音爆抵达时间
times_ori = data[:, 3:]

print(solve(locs, times_ori))
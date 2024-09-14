from utils import *

import numpy as np
from scipy import optimize as opt

data = np.array(
    [
        [110.241, 27.204, 824, 100.767],
        [110.780, 27.456, 727, 112.220],
        [110.712, 27.785, 742, 188.020],
        [110.251, 27.825, 850, 258.985],
        [110.524, 27.617, 786, 118.443],
        [110.467, 27.921, 678, 266.871],
        [110.047, 27.121, 575, 163.024]
    ]
)

locs = convert(data[:, 0:3], 'xyz')
times =   data[:, 3]
v = 0.34

@np.vectorize(excluded=[0])
def f(x, i):
    return distance(locs[i, :], x[0:3]) - (times[i] - x[3]) * v

def s(x):
    return np.sum(f(x, [0,1,2,3,5,6])**2)

constraint = [{'type': 'ineq', 'fun': lambda x: x[2]}]
result = opt.basinhopping(s, [0,0,0,0])
print(convert(np.array(result.x[0:3]), 'blh'))
print(result.x[3])
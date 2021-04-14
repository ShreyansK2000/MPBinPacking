from collections import namedtuple
import numpy as np
import math
from random import *
from decimal import *

def getNRandom(n=10):
    rands = []
    for i in range(n):
        rands.append(np.random.uniform(0,1,None))

    return rands

def getUniformVector(num_tasks):
    rands = getNRandom(num_tasks)
    # n = num_tasks

    # y_i = -log(x_i)
    randys = -1. * np.log(np.array(rands))

    # sum_randys = (y_1 + y_2 + .. y_n)
    sum_randys = np.sum(randys)
    
    return np.true_divide(randys, sum_randys)


def RandFixedSum(numTasks, numSets, minElemConstraint, maxElemConstraint, targetUtilization):

    # Check arguments
    if numTasks < 0 or numSets < 0:
        return []
    elif targetUtilization < numTasks * minElemConstraint or targetUtilization > numTasks * maxElemConstraint:
        return []

    # Rescale to a unit cube: 0 <= x(i) <= 1
    targetUtilization = (targetUtilization - numTasks * minElemConstraint) / (maxElemConstraint - minElemConstraint)

    # Construct the transition probability table t
    # t(i,j) will be utilized only in the region where j <= i + 1
    k = max(min(math.floor(targetUtilization), numTasks - 1), 0) # Must have  0 <= k <= n-1
    targetUtilization = max(min(targetUtilization, k + 1), k)    # Must have  k <= s <= k + 1

    # s1 and s2 are never negative
    s1 = targetUtilization - np.arange(k, k - numTasks, -1.)
    s2 = np.arange(k + numTasks, k, -1.) - targetUtilization

    # smallest (abs) and largest python float values
    tiny = np.finfo(float).tiny
    huge = np.finfo(float).max

    w = np.zeros((numTasks, numTasks + 1))
    w[0,1] = huge

    t = np.zeros((numTasks - 1, numTasks))

    for i in np.arange(2, numTasks + 1):
        tmp1 = w[i - 2, np.arange(1, i + 1)] * s1[np.arange(0, i)] / float(i)
        tmp2 = w[i - 2, np.arange(0, i)] * s2[np.arange(numTasks - i, numTasks)] / float(i)
        w[i - 1, np.arange(1, i + 1)] = tmp1 + tmp2
        tmp3 = w[i - 1, np.arange(1, i + 1)] + tiny # In case tmp1 & tmp2 are both 0
        tmp4 = s2[np.arange(numTasks - i, numTasks)] > s1[np.arange(0, i)] # then t is 0 on left & 1 on right
        t[i - 2, np.arange(0, i)] = (tmp2 / tmp3) * tmp4 + (1 - tmp1 / tmp3) * (np.logical_not(tmp4))

    #volume is never used...

    # Compute matrix x
    x = np.zeros((numTasks, numSets))

    # If m is zero, quit with x = []
    if numSets == 0: 
        return []

    rt = np.random.uniform(size=(numTasks - 1, numSets))  # For random selection of simplex type
    rs = np.random.uniform(size=(numTasks - 1, numSets))  # For random location within a simplex
    s = np.repeat(targetUtilization, numSets)
    j = np.repeat(k + 1, numSets)   # For indexing in the t table
    sm = np.repeat(0, numSets)      # Start with sum zero
    pr = np.repeat(1, numSets)      # Start with product 1
    
    for i in np.arange(numTasks - 1, 0, -1):  # Work backwards in the t table
        # Use rt to choose a transition
        e = rt[(numTasks - i) - 1, ...] <= t[i - 1, j - 1]
        sx = rs[(numTasks - i) - 1, ...] ** (1.0 / i)  # Use rs to compute next simplex coord.
        sm = sm + (1.0 - sx) * pr * s / (i + 1)     # update sum
        pr = sx * pr                                # update product
        x[(numTasks - i) - 1, ...] = sm + pr * e    # Calculate x using simplex coords.
        s = s - e
        j = j - e

    x[numTasks - 1, ...] = sm + pr * s

    #iterated in fixed dimension order but needs to be randomised
    #permute x row order within each column
    for i in range(0, numSets):
        x[..., i] = (maxElemConstraint - minElemConstraint) * x[np.random.permutation(numTasks), i] - minElemConstraint

    return x.T.tolist()

# Immutable task tuple, equivalent to something like a struct in C if it was immutable
Task = namedtuple("Task", ['Period', 'WCET', 'Utilization'])

# logU(a, b) ~ exp(U(log(a), log(b))
def lognuniform(low=10, high=1000000, base=10):
    return np.power(base, np.random.uniform(math.log(low), math.log(high), None))

def getTaskSet(utilization_vector, utilization):
    task_set = []
    for i in range(len(utilization_vector)):

        # FOR RTA run, don't need integer period and execution time
        # Different log uniform parameters
        # period = lognuniform(1, 6, 10)
        # wcet = utilization_vector[i] * period * utilization

        # FOR Simulation, need integer values for period and execution time
        Tg = 10
        period = math.floor(lognuniform(10, 1000000 + Tg, 10)/Tg) * Tg
        wcet = math.floor(utilization_vector[i] * period * utilization)

        task_set.append(Task(Period=period, WCET=wcet, Utilization=utilization_vector[i] * utilization))

    # See actual utilization by uncommenting this. Make sure few tasks per task, otherwise too many prints
    # print("utilization ", sum(float(task.WCET)/float(task.Period) for task in task_set))
    return task_set

# print(sum([round(y, 7) for y in RandFixedSum(10, 2, 0, 1, 3)[0]]))
print(sum(RandFixedSum(10, 2, 0, 1, 3)[0]))
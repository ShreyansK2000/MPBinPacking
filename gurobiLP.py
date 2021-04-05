import gurobipy as gp
from gurobipy import GRB
import numpy as np
import scipy.sparse as sp

taskSet = [
    0.1, 
    0.2,
    0.5,
    0.65,
    0.4,
]

def main():
    global taskSet

    n = len(taskSet)
    m = 3 # num processors or bins

    # matrix of decision variables x_ij
    DecisionVariableMatrixShape = (n,m)
    # = np.zeros(shape)

    model = gp.Model()

    TaskSetUtilizationsVector = np.asarray(taskSet)

    TaskUsedConstraintVector = np.ones(m, dtype=np.int)
    TaskUsedResultVector = np.ones(n, dtype=np.int)

    print("Utilization Vector: ", TaskSetUtilizationsVector)
    print("Task Used Constraint Vector: ", TaskUsedConstraintVector)
    print("Task Used Result Vector: ", TaskUsedResultVector)

    DecisionVariableMatrix = model.addMVar(DecisionVariableMatrixShape, vtype=GRB.BINARY)
    ProcessorsUsedVector = model.addMVar(m, vtype=GRB.BINARY)   

    # Some testing related prints, figuring out dimensions with GRBPy
    # print(DecisionVariableMatrix[:,1])
    # print(sum(DecisionVariableMatrix[:,1]))
    # print(ProcessorsUsedVector[0])
    # print(DecisionVariableMatrix[i, 1] * TaskSetUtilizationsVector[i] for i in range(n))

    model.setObjective(sum(ProcessorsUsedVector), GRB.MINIMIZE)

    # for each row, sum(row) should be 1,
    # This constraint checks that each task is used exactly once in the assignment
    model.addConstrs(sum(DecisionVariableMatrix[i, :]) == 1 for i in range(n))

    model.addConstrs(sum(DecisionVariableMatrix[i, j] * TaskSetUtilizationsVector[i] for i in range(n)) <= ProcessorsUsedVector[j] for j in range(m))

    model.optimize()

    print("number of bins: ", model.ObjVal)


if __name__ == "__main__":
    main()
from tasksetgeneration import *
from gurobiLP import *
from approxBinPacking import *
import time
import matplotlib.pyplot as plt

numTaskSetsPerTest = 20
taskSetSizes = [8, 16, 32, 64, 128, 256]
# targetUtilizations = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
targetUtilizations = [2.8, 2.9, 2.95, 2.99, 3., 3.5, 4, 4.5, 5]

def main():

    # avgFFDDurationsPerU = []
    # avgILPDurationsPerU = []
    for u in targetUtilizations:
        print("------------------- u = {}--------------------".format(u))

        # collect information of runtime per task set size
        avgResDiffs = []
        varianceResDiffs = []
        avgFFDDurations = []
        avgILPDurations = []
        # avgILPResults = []

        for numTasks in taskSetSizes:
            print("\t*************** n = {} ******************".format(numTasks))
            # if numTasks < u:
            #     continue

            # collect information of runtime per task set size
            resDiffs = []
            ffdDurations = []
            ilpDurations = []

            # ffdResults = []
            # ilpResults = []

            taskSets = RandFixedSum(numTasks, numTaskSetsPerTest, 0, 1, u)

            for i, taskSet in enumerate(taskSets):

                ffdStart = time.perf_counter_ns()
                resFFD = ffd_pack(taskSet, numTasks)
                ffdEnd = time.perf_counter_ns()
                ffdDuration = ffdEnd - ffdStart
                ffdDurations.append(ffdDuration)

                ilpStart = time.perf_counter_ns()
                resILP = ilp_pack(taskSet, numTasks)
                ilpEnd = time.perf_counter_ns()
                ilpDuration = ilpEnd - ilpStart
                ilpDurations.append(ilpDuration)

                resDiff = -1

                if resFFD > 0 and resILP > 0:
                    resDiff = resFFD - resILP
                
                resDiffs.append(resDiff)
                # ilpResults.append(resILP)

                print("finished a task set {}".format(i))

            # print("resDiffs: ", resDiffs)
            avgResDiffs.append(np.mean(resDiffs))
            varianceResDiffs.append(np.var(resDiffs))

            # print("ffdDurations: ", ffdDurations)
            avgFFDDurations.append(np.mean(ffdDurations))

            # print("ilpDurations: ", ilpDurations)
            avgILPDurations.append(np.mean(ilpDurations))

            # avgILPResults.append(np.mean)

        fig = plt.figure(figsize=(16, 8))

        ax1 = fig.add_subplot(121)
        ax1.plot(np.log2(taskSetSizes), avgFFDDurations, marker='.', markerfacecolor='blue', markersize=18, color='skyblue', linewidth=4, label="Average FFD Packing runtime")
        ax1.plot(np.log2(taskSetSizes), avgILPDurations, marker='^',markerfacecolor='red', markersize=10, color='lightcoral', linewidth=4, label="Average ILP Packing runtime")
        ax1.set_title('Runtime Comparison')
        ax1.set_xlabel('Task Set Size')
        ax1.set_ylabel('Time Taken (ns)')
        ax1.legend(loc="best")

        ax2 = fig.add_subplot(122)
        ax2.plot(np.log2(taskSetSizes), avgResDiffs, marker='.', markerfacecolor='blue', markersize=18, color='skyblue', linewidth=4, label="Average Difference in FFD and ILP Results")
        ax2.plot(np.log2(taskSetSizes), varianceResDiffs, marker='^',markerfacecolor='red', markersize=10, color='lightcoral', linewidth=4, label="Variance of Difference in FFD and ILP Results")
        ax2.set_title('Mean and Variance Comparison')
        ax2.set_xlabel('Task Set Size')
        ax2.set_ylabel('Value')
        ax2.legend(loc="best")

        fig.suptitle("Utilization = {}".format(u), fontsize=16)

        plt.savefig('figs/{}-util-runtime-comparison.png'.format(u))
        # plt.show()
        # ax = fig.add_subplot(111,projection='3d')
        print("finished u = {}\n".format(u))

if __name__ == "__main__":
    main()
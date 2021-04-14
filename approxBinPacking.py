import time

# Helper function to sum the utilization associated with 
# each processor
# TODO make more efficient by not needing to sum every time
# DP with a per-processor current utilization value
def getProcessorUtilization(processorTasks):
    return sum(taskUtil for taskUtil in processorTasks)

# For now just FFD, extend this with other approximate bin packing heuristics
def ffd_pack(taskSet, processorUB):
    # global taskSet # TODO change this so that we can add a larger number of tests
    
    # m: the maximum number of processors allowed
    numProcessors = processorUB

    # A list of lists that tracks the tasks (tuples) assigned to each processor
    processors = []

    # The index of the most recently opened processor bin
    currentProcessor = 0

    # Sort to be in non-increasing order
    # tuples are sorted by default on the first item in the tuple
    taskSet.sort(reverse=True)

    # print("ffd start", time.perf_counter_ns())

    for taskUtil in taskSet:
        # If there is at least one task, open the first bin
        if len(processors) == 0:
            processors.append([])
        
        assigned = False
        for i in range(len(processors)):
            if taskUtil + getProcessorUtilization(processors[i]) <= 1:
                processors[i].append(taskUtil)
                assigned = True
                break
        
        # If a task is not assigned that means there is
        # not enough space in existing bins! Open a new
        # bin if possible under constraints
        if not assigned:
            if len(processors) < numProcessors - 1:
                processors.append([])
                currentProcessor += 1
                if taskUtil + getProcessorUtilization(processors[currentProcessor]) <= 1:
                    processors[currentProcessor].append(taskUtil)
                    assigned = True
            else:
                print("Exceeded number of processors that can be used!! Not schedulable!")
                return -1

    # print("ffd end", time.perf_counter_ns())

    # print("Scheduled~~!!")
    # print(processors)
    return len(processors)


if __name__ == "__main__" :
    taskSet = [
        0.1, 
        0.2,
        0.5, 
        0.65,
        0.4 
    ]
    ffd_pack(taskSet, len(taskSet))
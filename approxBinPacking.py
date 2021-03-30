taskSet = [
    (0.1, 10), 
    (0.2, 15),
    (0.5, 8),
    (0.65, 12),
    (0.4, 20)
]

# Helper function to sum the utilization associated with 
# each processor
# TODO make more efficient by not needing to sum every time
# DP with a per-processor current utilization value
def getProcessorUtilization(processorTasks):
    return sum(task[0] for task in processorTasks)

# For now just FFD, extend this with other approximate bin packing heuristics
def main():
    global taskSet # TODO change this so that we can add a larger number of tests
    
    # m: the maximum number of processors allowed
    numProcessors = 3

    # A list of lists that tracks the tasks (tuples) assigned to each processor
    processors = []

    # The index of the most recently opened processor bin
    currentProcessor = 0

    # Sort to be in non-increasing order
    # tuples are sorted by default on the first item in the tuple
    taskSet.sort(reverse=True)

    for task in taskSet:
        # If there is at least one task, open the first bin
        if len(processors) == 0:
            processors.append([])
        
        assigned = False
        for i in range(len(processors)):
            if task[0] + getProcessorUtilization(processors[i]) <= 1:
                processors[i].append(task)
                assigned = True
                break
        
        # If a task is not assigned that means there is
        # not enough space in existing bins! Open a new
        # bin if possible under constraints
        if not assigned:
            if len(processors) < numProcessors - 1:
                processors.append([])
                currentProcessor += 1
                if task[0] + getProcessorUtilization(processors[currentProcessor]) <= 1:
                    processors[currentProcessor].append(task)
                    assigned = True
            else:
                print("Exceeded number of processors that can be used!! Not schedulable!")

    print("Scheduled~~!!")
    print(processors)
    return


if __name__ == "__main__" :
    main()
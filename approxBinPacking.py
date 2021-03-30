taskSet = [
    (0.1, 10), 
    (0.2, 15),
    (0.5, 8),
    (0.65, 12),
    (0.4, 20)
]

def getProcessorUtilization(processorTasks):
    return sum(task[0] for task in processorTasks)

# For now just FFD, extend this with other approximate bin packing
def main():
    global taskSet
    numProcessors = 3
    processors = []
    currentProcessor = 0

    # Sort to be in non-increasing order
    # tuples are sorted by default on the first item in the tuple
    taskSet.sort(reverse=True)

    for task in taskSet:
        if len(processors) == 0:
            processors.append([])
        
        assigned = False
        for i in range(len(processors)):
            if task[0] + getProcessorUtilization(processors[i]) <= 1:
                processors[i].append(task)
                assigned = True
                break
        
        # not enough space in existing bins!
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
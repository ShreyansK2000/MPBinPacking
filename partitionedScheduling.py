import math
from operator import itemgetter
import multiset
from functools import reduce

EPSILON = 0.3
NUM_PROCESSORS = 4
testedSingleProcessorConfigs = set()
testedMultiProcessorConfigs = []


def getSingleProcessorUtilization(singleProcConfig, VEpsilon):
    return sum([singleProcConfig[i] * VEpsilon[i] for i in range(len(VEpsilon))])

def getMultiProcessorUtilization(multiProcConfig, L1Epsilon, VEpsilon):
    singleProcConfigs = []
    for i in multiProcConfig:
        if i != -1:
            singleProcConfigs.append(L1Epsilon[i])
    return sum([getSingleProcessorUtilization(config, VEpsilon) for config in singleProcConfigs])

def maximalSingleProcessorConfigDFS(prevConfig, VEpsilon):
    # global testedConfigs
    configsToReturn = []
    
    if tuple(prevConfig) in testedSingleProcessorConfigs:
        return []

    for i in range(len(VEpsilon)):
        currentConfig = prevConfig.copy()
        currentConfig[i] += 1

        configs = None
        currentUtilization = getSingleProcessorUtilization(currentConfig, VEpsilon)

        if currentUtilization < 1:
            configs = maximalSingleProcessorConfigDFS(currentConfig, VEpsilon)
            
            if len(configs) == 0:
                configsToReturn.append(currentConfig)
                continue

            for i in range(len(configs)):
                if getSingleProcessorUtilization(configs[i], VEpsilon) > 1 - EPSILON:
                    configsToReturn.append(configs[i])
        
        elif currentUtilization == 1:
            configsToReturn.append(currentConfig)

    testedSingleProcessorConfigs.add(tuple(prevConfig))
    return configsToReturn

def getSingleProcessorMaximalConfigs(VEpsilon):
    validMaximalConfigs = []
    defaultConfig = [0] * len(VEpsilon)
    
    for i in range(len(VEpsilon)):
        currentConfig = defaultConfig.copy()
        currentConfig[i] = 1

        configs = None
        currentUtilization = getSingleProcessorUtilization(currentConfig, VEpsilon)

        if currentUtilization < 1:
            configs = maximalSingleProcessorConfigDFS(currentConfig, VEpsilon)
            
            if len(configs) == 0:
                validMaximalConfigs.append(currentConfig)
                continue

            for i in range(len(configs)):
                if getSingleProcessorUtilization(configs[i], VEpsilon) > 1 - EPSILON:
                    validMaximalConfigs.append(configs[i])
        
        elif currentUtilization == 1:
            validMaximalConfigs.append(currentConfig)

    maximalConfigurations = set(tuple(config) for config in validMaximalConfigs)
    return maximalConfigurations

def generateMutliProcessorConfigDFS(prevMultiConfig, prevProcessorIdx, L1Epsilon, VEpsilon):
    configsToReturn = []
    
    if multiset.Multiset(tuple(prevMultiConfig)) in testedMultiProcessorConfigs:
        # print('here ', prevMultiConfig)
        return configsToReturn

    # return if we have reached the max length of the multiprocessor config
    if prevProcessorIdx == NUM_PROCESSORS - 1:
        # print('here 2 ', prevMultiConfig)
        return configsToReturn

    for i in range(len(L1Epsilon)):
        currentMultiConfig = prevMultiConfig.copy()
        currentIdx = prevProcessorIdx + 1
        currentMultiConfig[currentIdx] = i
        # print(currentMultiConfig)

        configs = None
        currentUtilization = getMultiProcessorUtilization(currentMultiConfig, L1Epsilon, VEpsilon)

        if currentUtilization < NUM_PROCESSORS:

            if currentMultiConfig[-1] != -1:
                testedMultiProcessorConfigs.append(multiset.Multiset(tuple(currentMultiConfig)))
                configsToReturn.append(currentMultiConfig)

            else:
                configs = generateMutliProcessorConfigDFS(currentMultiConfig, currentIdx, L1Epsilon, VEpsilon)
                
                if len(configs) == 0:
                    configsToReturn.append(currentMultiConfig)
                    continue

                for i in range(len(configs)):
                    # if getSingleProcessorUtilization(configs[i], VEpsilon) > 1 - EPSILON:
                    if -1 not in configs[i]:
                        configsToReturn.append(configs[i])
                    # configsToReturn.append(configs[i])
        
        elif currentUtilization == NUM_PROCESSORS:
            configsToReturn.append(currentMultiConfig)

    testedMultiProcessorConfigs.append(multiset.Multiset(tuple(prevMultiConfig)))
    return configsToReturn

def getMultiProcessorConfigs(L1Epsilon, VEpsilon):
    validMaximalConfigs = []
    defaultConfig = [-1] * NUM_PROCESSORS
    # print(defaultConfig)

    for i in range(len(L1Epsilon)):
        currentMultiConfig = defaultConfig.copy()
        currentMultiConfig[0] = i
        processorIdx = 0

        configs = None
        currentUtilization = getMultiProcessorUtilization(currentMultiConfig, L1Epsilon, VEpsilon)

        if currentUtilization < NUM_PROCESSORS:
            configs = generateMutliProcessorConfigDFS(currentMultiConfig, processorIdx, L1Epsilon, VEpsilon)
            # print(configs)
            
            if len(configs) == 0:
                validMaximalConfigs.append(currentMultiConfig)
                continue

            for i in range(len(configs)):
                # if getSingleProcessorUtilization(configs[i], VEpsilon) > 1 - EPSILON:
                if -1 not in configs[i]:
                    validMaximalConfigs.append(configs[i])
        
        elif currentUtilization == NUM_PROCESSORS:
            validMaximalConfigs.append(currentMultiConfig)

    maximalConfigurations = set(tuple(config) for config in validMaximalConfigs)
    return maximalConfigurations


def main():
    VSize = math.floor(math.log(1 / EPSILON) / math.log(1 + EPSILON)) + 1
    VEpsilon = [EPSILON * ((1 + EPSILON)**i) for i in range(VSize)]

    # Testing that V has all elements possible <= 1
    print(VEpsilon)
    # print(VEpsilon[-1] * (1 + epsilon))

    # L1Epsilon is an ordered list of maximal single processor configurations
    L1Epsilon = list(getSingleProcessorMaximalConfigs(VEpsilon))
    L1Epsilon.sort(key=lambda config: getSingleProcessorUtilization(config, VEpsilon))
    print("Single Processor Maximal Configurations:", L1Epsilon)

    testedSingleProcessorConfigs.clear()

    validMultiProcessorConfigurations = getMultiProcessorConfigs(L1Epsilon, VEpsilon)
    # print(validMultiProcessorConfigurations)
    # print(len(validMultiProcessorConfigurations))

    # Construct the map
    mapMulti = {}
    for singleProcessIndexTuple in validMultiProcessorConfigurations:
        multiProcessorTuple = (0, ) * len(VEpsilon)
        for singleProcessIndex in singleProcessIndexTuple:
            multiProcessorTuple = tuple([sum(x) for x in zip(multiProcessorTuple, L1Epsilon[singleProcessIndex])])
        mapMulti[singleProcessIndexTuple] = multiProcessorTuple 
    
    # print(mapMulti)
    # print(len(mapMulti))

    rejectedSet = set()
    acceptedSet = set()
    for mapKey in validMultiProcessorConfigurations:
        rejected = False
        for k, v in mapMulti.items():
            if mapKey == k:
                continue

            diffTuple = [x >= y for x, y in zip(v, mapMulti[mapKey])]
            # print(diffTuple)
            allGreater = reduce(lambda x, y: x and y, diffTuple)

            # diffbool =  all(diff >= 0 for diff in diffTuple)
            # rejected = not diffbool
            # print(diffbool)
            if allGreater:
                # if there are any other tuples with all y' >= y for all i in len(L1Epsilon) 
                rejectedSet.add(mapKey)
                break
        if rejected:
            acceptedSet.add(mapKey)

        
    result = validMultiProcessorConfigurations.difference(rejectedSet)
    # print(result)
    # print(acceptedSet)
    print(len(result))
    print(len(acceptedSet))

    # for i in acceptedSet:
    #     print(mapMulti[i])

if __name__ == "__main__":
    main()
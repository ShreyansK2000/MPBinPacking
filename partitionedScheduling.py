import math

EPSILON = 1/9
testedConfigs = set()

def getUtilization(config, VEpsilon):
    return sum([config[i] * VEpsilon[i] for i in range(len(VEpsilon))])


def getFullConfigs(prevConfig, VEpsilon):
    # global testedConfigs
    configsToReturn = []
    
    if tuple(prevConfig) in testedConfigs:
        return []

    for i in range(len(VEpsilon)):
        currentConfig = prevConfig.copy()
        currentConfig[i] += 1

        # if tuple(currentConfig) in testedConfigs:
        #     continue
        # else:
        #     testedConfigs.add(tuple(currentConfig))

        configs = None
        currentUtilization = getUtilization(currentConfig, VEpsilon)

        if currentUtilization < 1:
            configs = getFullConfigs(currentConfig, VEpsilon)
            
            if len(configs) == 0:
                configsToReturn.append(currentConfig)
                continue

            for i in range(len(configs)):
                if getUtilization(configs[i], VEpsilon) > 1 - EPSILON:
                    configsToReturn.append(configs[i])
        
        elif currentUtilization == 1:
            configsToReturn.append(currentConfig)

    testedConfigs.add(tuple(prevConfig))
    return configsToReturn

def getMaximalConfigs(VEpsilon):
    maximalConfigurations = []
    defaultConfig = [0] * len(VEpsilon)
    # print(defaultConfig)
    
    for i in range(len(VEpsilon)):
        currentConfig = defaultConfig.copy()
        currentConfig[i] = 1

        configs = None
        currentUtilization = getUtilization(currentConfig, VEpsilon)

        if currentUtilization < 1:
            configs = getFullConfigs(currentConfig, VEpsilon)
            
            if len(configs) == 0:
                maximalConfigurations.append(currentConfig)
                continue

            for i in range(len(configs)):
                if getUtilization(configs[i], VEpsilon) > 1 - EPSILON:
                    maximalConfigurations.append(configs[i])
        
        elif currentUtilization == 1:
            maximalConfigurations.append(currentConfig)

        # if sum(fullConfig) > (1 - epsilon):
        #     maximalConfigurations.append(fullConfig)

    maximalConfigurations = set(tuple(config) for config in maximalConfigurations)
    return maximalConfigurations


def main():
    VSize = math.floor(math.log(1 / EPSILON) / math.log(1 + EPSILON)) + 1
    VEpsilon = [EPSILON * ((1 + EPSILON)**i) for i in range(VSize)]

    # Testing that V has all elements possible <= 1
    print(VEpsilon)
    # print(VEpsilon[-1] * (1 + epsilon))

    maximalConfigurations = getMaximalConfigs(VEpsilon)
    print(len(maximalConfigurations))

if __name__ == "__main__":
    main()
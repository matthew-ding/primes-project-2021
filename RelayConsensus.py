import copy
import random
import numpy as np
import graphGenerator


class Node:
    def __init__(self, n, m, value):
        self.num = n
        self.parameterList = {n: Parameter(value, 0.0)}
        self.m = m

    def getParams(self):
        return self.parameterList

    def __str__(self):
        output = ""
        for i in range(self.m):
            if i in self.getParams():
                output += "Parameter " + str(i) + ": " + str(self.getParams()[i].getParams()) + "\n"
            else:
                output += "Parameter " + str(i) + ": NONE" + "\n"

        return output + "\n"


class Parameter:
    def __init__(self, n, it):
        self.iter = it
        self.params = n

    def getIter(self):
        return self.iter

    def getParams(self):
        return self.params


def trimmed_mean(X, f):
    sorted_X = np.sort(X)
    size = len(sorted_X)
    sorted_X = sorted_X[f:size - f]

    return sum(sorted_X) / len(sorted_X)


# random byzantine parameters
def byzantine_function(x):
    return random.randrange(-5.0 * x, 10.0 * x)


# deviation of honest parameters
def getDeviation(nodeList, m, byzantine_set):
    array = []
    for i in range(m):
        if i not in byzantine_set:
            array.append(nodeList[i].getParams()[i].getParams())

    return np.array(array).std()


def broadcast(nodeList, m, adjList, byzantine_set):
    tempNodeList = copy.deepcopy(nodeList)  # node list before broadcast starts
    for i in range(m):
        if i not in byzantine_set:  # byzantine nodes don't store other node's data
            for j in adjList[i]:
                if j in byzantine_set:
                    tempNodeList[j].parameterList[j] = Parameter(byzantine_function(i), iters - 1)

                tempNeighbor = tempNodeList[j].getParams()
                currentParamList = nodeList[i].parameterList

                # updating parameters to newest iteration
                for key in tempNeighbor:
                    if key not in currentParamList:
                        currentParamList[key] = tempNeighbor[key]
                    elif currentParamList[key].getIter() < tempNeighbor[key].getIter():
                        currentParamList[key] = tempNeighbor[key]


# Approximate Byzantine Consensus (relay version)
def IABC(iters, nodeList, m, adjList, diameter, maxIter, byzantine_set, updateFreq):
    while True:
        # neighbor aggregation
        broadcast(nodeList, m, adjList, byzantine_set)

        for i in range(m):
            if iters >= diameter and iters % updateFreq == 0 and i not in byzantine_set:
                theta = nodeList[i].parameterList

                parameterArray = []
                for j in theta:
                    parameterArray.append(theta[j].getParams())

                # Trimmed mean
                theta[i] = Parameter(trimmed_mean(parameterArray, len(byzantine_set)), iters)

        # print if update iteration
        if iters % updateFreq == 0 and iters >= diameter:
            print("Iteration " + str(iters))

            std = getDeviation(nodeList, m, byzantine_set)
            print("Standard Deviation " + str(std))

            if std < 0.01:
                break

            # printAll(nodeList, m, byzantine_set)

        if iters > maxIter:
            break

        iters += 1

    return nodeList, iters


def printAll(nodeList, m, byzantine_set):
    for i in range(m):
        if i not in byzantine_set:
            print("NODE: " + str(i))
            print(nodeList[i].getParams()[i].getParams())


diameter = 10
maxIter = 1000
updateFreq = 1

# Graph generation
adjList, byzantine_set, m, target = graphGenerator.get_relay_graph(diameter)
print("Graph Generated Successfully")

nodeList = []  # list of all nodes

for i in range(m):
    # parameter arrays
    nodeList.append(Node(i, m, 1.0 * random.randrange(9, 110)))

iters = 1

g, iters = IABC(iters, nodeList, m, adjList, diameter, maxIter, byzantine_set, updateFreq)

print("Converges in " + str(iters) + " iterations")
printAll(g, m, byzantine_set)

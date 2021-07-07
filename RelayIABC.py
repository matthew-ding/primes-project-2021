import copy
import random
from decimal import Decimal
import numpy as np


class Node:
    def __init__(self, n, value):
        self.num = n
        self.parameterList = {n: Decimal(value)}

    def getParamList(self):
        return self.parameterList

    def setSelfParam(self, value):
        self.parameterList[self.num] = value

    def getSelfParam(self):
        return self.getParamList()[self.num]


def trimmed_mean(X, f):
    sorted_X = np.sort(X)
    size = len(sorted_X)
    sorted_X = sorted_X[f:size - f]
    return sum(sorted_X) / len(sorted_X)


# random byzantine parameters
def byzantine_function(x):
    return Decimal(random.randrange((x-20)*1000, (x+20)*1000)/1000)


# deviation of honest parameters
def getDeviation(nodeList, m, byzantine_set):
    array = []
    for i in range(m):
        if i not in byzantine_set:
            array.append(nodeList[i].getSelfParam())

    return np.array(array).std()


# range of honest parameters
def getRange(nodeList, m, byzantine_set):
    array = []
    for i in range(m):
        if i not in byzantine_set:
            array.append(nodeList[i].getSelfParam())

    return np.ptp(np.array(array))


def broadcast(nodeList, m, adjList, byzantine_set):
    tempNodeList = copy.deepcopy(nodeList)  # node list before broadcast starts
    for i in range(m):
        if i not in byzantine_set:  # byzantine nodes don't store other node's data
            for j in adjList[i]:
                if j in byzantine_set:
                    tempNodeList[j].setSelfParam(byzantine_function(-110 + (i+j)*110/m))

                tempNeighbor = tempNodeList[j].parameterList
                currentParamList = nodeList[i].parameterList

                # updating parameters to newest iteration
                for key in tempNeighbor:
                    currentParamList[key] = tempNeighbor[key]


# Iterative Approximate Byzantine Consensus (relay version)
def main(iters, maxIter, adjList, byzantine_set, m, diameter, nodeList):
    stdList = []
    rangeList = []

    while True:
        # broadcast step
        broadcast(nodeList, m, adjList, byzantine_set)

        # aggregation step
        if iters % diameter == 0:
            for i in range(m):
                if i not in byzantine_set:
                    parameterArray = []
                    for j in range(m):
                        parameterArray.append(nodeList[i].getParamList()[j])

                    # Trimmed mean
                    nodeList[i].setSelfParam(trimmed_mean(parameterArray, len(byzantine_set)))

            # resetting arrays
            for i in range(m):
                if i not in byzantine_set:
                    nodeList[i].parameterList = {i: nodeList[i].getSelfParam()}

        if iters > maxIter:
            break

        iters += 1

        # standard deviation
        std = getDeviation(nodeList, m, byzantine_set)
        stdList.append(std)

        # range
        range1 = getRange(nodeList, m, byzantine_set)
        rangeList.append(range1)

    return iters, nodeList, m, byzantine_set, stdList, rangeList


def printAll(nodeList, m, byzantine_set):
    for i in range(m):
        if i not in byzantine_set:
            print("NODE: " + str(i))
            print(nodeList[i].getSelfParam())



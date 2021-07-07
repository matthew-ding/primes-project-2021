import copy
import random
from decimal import Decimal
import numpy as np


class Node:
    def __init__(self, n, value):
        self.num = n
        self.parameter = value

    def getParams(self):
        return self.parameter


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
            array.append(nodeList[i].getParams())

    return np.array(array).std()


# range of honest parameters
def getRange(nodeList, m, byzantine_set):
    array = []
    for i in range(m):
        if i not in byzantine_set:
            array.append(nodeList[i].getParams())

    return np.ptp(np.array(array))


# Itertive Approximate Byzantine Consensus (non-relay version)
def main(iters, maxIter, adjList, byzantine_set, m, nodeList):
    stdList = []
    rangeList = []
    while True:
        tempNodeList = copy.deepcopy(nodeList)  # node list before broadcast starts

        # aggregation step
        for i in range(m):
            if i not in byzantine_set:
                parameterArray = [tempNodeList[i].getParams()]

                for j in adjList[i]:
                    if j in byzantine_set:
                        tempNodeList[j].parameter = byzantine_function(-110 + (i+j)*110/m)

                    parameterArray.append(tempNodeList[j].getParams())

                # Trimmed mean
                nodeList[i].parameter = trimmed_mean(parameterArray, len(byzantine_set))

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
            print(nodeList[i].getParams())

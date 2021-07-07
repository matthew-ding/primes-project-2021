import copy
import random
from decimal import Decimal
import RelayIABC
import IABC
import graphGenerator
import matplotlib.pyplot as plt
import numpy as np

# hyperparameters
maxIter = 100
hsize = 30

# Graph generation
adjList, byzantine_set, m, diameter, density = graphGenerator.get_random_graph(hsize)

# Node initialization
valueList = []
for i in range(m):
    valueList.append(Decimal(random.randrange(-110, 110)))

masterNodeList = {}
masterRelayNodeList = {}
for i in range(m):
    masterNodeList[i] = IABC.Node(i, valueList[i])
    masterRelayNodeList[i] = RelayIABC.Node(i, valueList[i])

list1 = []
list2 = []
list3 = []
list4 = []

# driver functions
for repetitions in range(10):
    print("Repetition: " + str(repetitions))
    # Standard IABC
    iters = 1
    nodeList = copy.deepcopy(masterNodeList)
    iters, finalNodeList, m, byzantine_set, stdList1, rangeList1 = IABC.main(iters, maxIter, adjList, byzantine_set, m, nodeList)
    list1.append(stdList1)
    list3.append(rangeList1)

    # Relay IABC
    iters = 1
    relayNodeList = copy.deepcopy(masterRelayNodeList)
    iters, finalNodeList, m, byzantine_set, stdList2, rangeList2 = RelayIABC.main(iters, maxIter, adjList, byzantine_set, m,
                                                                      diameter,
                                                                      relayNodeList)
    list2.append(stdList2)
    list4.append(rangeList2)


list1 = np.mean(np.array(list1), axis=0, dtype=np.float64)
list2 = np.mean(np.array(list2), axis=0, dtype=np.float64)
list3 = np.mean(np.array(list3), axis=0, dtype=np.float64)
list4 = np.mean(np.array(list4), axis=0, dtype=np.float64)

# standard deviation plot
plt.plot([i for i in range(1, maxIter + 1)], list1, label="IABC")
plt.plot([i for i in range(1, maxIter + 1)], list2, label="RelayIABC")
plt.title("IABC vs. RelayIABC Standard Deviation")
plt.xlabel("Iteration")
plt.ylabel('Standard Deviation')
plt.yscale("log")
plt.legend()
plt.show()
plt.clf()

"""
# range plot
plt.plot([i for i in range(1, maxIter + 1)], list3, label="IABC")
plt.plot([i for i in range(1, maxIter + 1)], list4, label="RelayIABC")
plt.title("IABC vs. RelayIABC Range")
plt.xlabel("Iteration")
plt.ylabel('Range')
plt.yscale("log")
plt.legend()
plt.show()
plt.clf
"""



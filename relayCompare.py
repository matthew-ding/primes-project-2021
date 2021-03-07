import copy
import random
import RelayConsensus
from graphGenerator import get_relay_graph
import matplotlib.pyplot as plt

# hyperparameters
bsize = 15
maxIter = 200
accuracy = 0.03
iters = 1

stdList = []
freqList = []

# Graph generation
adjList, byzantine_set, m, diameter = get_relay_graph(bsize)
print("Graph Generated Successfully")

# Node initialization
nodeList = []  # list of all nodes
for i in range(m):
    nodeList.append(RelayConsensus.Node(i, m, 1.0 * random.randrange(-110, 110)))


for i in range(1, 2 * bsize + 5):
    tempNodeList = copy.deepcopy(nodeList)
    updateFreq = i

    # driver function
    finalIters, finalNodeList, m, byzantine_set, std = RelayConsensus.IABC(iters, maxIter, updateFreq, accuracy,
                                                                           adjList, byzantine_set, m, diameter,
                                                                           tempNodeList)
    freqList.append(updateFreq)
    stdList.append(std)

    print("Update Frequency: " + str(updateFreq))
    print("Standard Deviation: " + str(std))

plt.plot(freqList, stdList)
plt.title('Relay Speed vs. Update Frequency')
plt.xlabel("Update Frequency")
plt.ylabel('Standard Deviation')
plt.yscale("log")
plt.show()

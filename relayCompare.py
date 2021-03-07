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
itersList = []

# Graph generation
adjList, byzantine_set, m, diameter = get_relay_graph(bsize)
print("Graph Generated Successfully")

# Node initialization
nodeList = []  # list of all nodes
for i in range(m):
    # parameter arrays
    nodeList.append(RelayConsensus.Node(i, m, 1.0 * random.randrange(-110, 110)))

for i in range(1, 3*bsize):
    updateFreq = i
    print("Update Frequency: " + str(updateFreq))
    # driver function
    finalIters, finalNodeList, m, byzantine_set, std = RelayConsensus.IABC(iters, maxIter, updateFreq, accuracy, adjList, byzantine_set, m, diameter, nodeList)
    stdList.append(updateFreq)
    itersList.append(finalIters)


plt.plot(stdList, itersList)
plt.title('Relay Speed vs. Update Frequency')
plt.xlabel('Iterations per Update')
plt.ylabel('Standard Deviation')
plt.show()





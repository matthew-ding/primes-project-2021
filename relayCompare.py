import copy
import random
import RelayConsensus
import graphGenerator
import matplotlib.pyplot as plt

# hyperparameters
hsize = 100
bsize = 15
maxIter = 300
accuracy = 0.03
iters = 1

stdList = []
freqList = []

# Graph generation
adjList, byzantine_set, m, diameter, density = graphGenerator.get_random_graph(200)
print("Graph Generated Successfully")
print("Size: " + str(m))
print("Diameter: " + str(diameter))
print("Density: " + str(density))

# Node initialization
nodeList = []  # list of all nodes
for i in range(m):
    nodeList.append(RelayConsensus.Node(i, m, 1.0 * random.randrange(-110, 110)))


for i in range(1, diameter+1):
    print(" ")
    print("Update Frequency: " + str(i))
    print(" ")
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
plt.title("Nodes: " + str(m) + ", " + "Diameter: " + str(diameter) + ", Density: " + str(density))
plt.xlabel("Update Frequency")
plt.ylabel('Standard Deviation')
plt.yscale("log")
plt.show()
plt.savefig("figure2")

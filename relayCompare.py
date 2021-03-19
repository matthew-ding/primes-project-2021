import copy
import random
import RelayConsensus
import graphGenerator
import matplotlib.pyplot as plt

# hyperparameters
hsize = 100
bsize = 15
maxIter = 1000
accuracy = 0.03
iters = 1

stdList = []
freqList = []

# Graph generation
adjList, byzantine_set, m, diameter, density = graphGenerator.get_linear_graph(50)
print("Graph Generated Successfully")
print("Size: " + str(m))
print("Diameter: " + str(diameter))
print("Density: " + str(density))

# Node initialization
nodeList = [RelayConsensus.Node(0, 0, 0)] * m  # list of all nodes
valueList = []  # list of all initial node values
# creating list of initial values
for i in range(m):
    valueList.append(1.0 * random.randrange(-110, 110))


for i in range(1, diameter + 1):
    freqList.append(i)
    tempStdList = []
    for repetitions in range(5):
        for j in range(m):
            nodeList[j] = RelayConsensus.Node(j, m, valueList[j])
        print(" ")
        print("Update Frequency: " + str(i))
        print(" ")
        tempNodeList = copy.deepcopy(nodeList)
        updateFreq = i

        # driver function
        finalIters, finalNodeList, m, byzantine_set, std = RelayConsensus.IABC(iters, maxIter, updateFreq, accuracy,
                                                                               adjList, byzantine_set, m, diameter,
                                                                               tempNodeList)

        tempStdList.append(std)
    stdList.append(sum(tempStdList) / len(tempStdList))
    print("Update Frequency: " + str(i))
    print("Standard Deviation: " + str(sum(tempStdList) / len(tempStdList)))

plt.plot(freqList, stdList)
plt.title("Nodes: " + str(m) + ", " + "Diameter: " + str(diameter) + ", Density: " + str(density))
plt.xlabel("Update Frequency")
plt.ylabel('Standard Deviation')
plt.yscale("log")
plt.show()
plt.savefig("figure2")

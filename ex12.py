import numpy as np
from scipy.optimize import linprog
from basic_utils import nn2na
import random
import networkx as nx
import matplotlib.pyplot as plt

# Initialize points

random.seed(50)

NN = np.zeros((6, 6))
startingPoint = 0

while startingPoint < 5:
    destinationPoint = startingPoint + 1
    while destinationPoint <= 5:
        distance = random.randint(1, 100)
        NN[startingPoint][destinationPoint] = distance
        NN[destinationPoint][startingPoint] = distance
        destinationPoint = destinationPoint + 1
    startingPoint = startingPoint + 1


NA = nn2na(NN)
Aeq1 = NA.copy()
Aeq1 = np.where(Aeq1 == 1, Aeq1, 0)
Aeq2 = NA.copy()
Aeq2 = np.where(Aeq2 == -1, 1, 0)

Aeq = np.concatenate((Aeq1, Aeq2))

distances = np.empty(0)
i = 0
while i < Aeq.shape[1]:
    indexes = np.argwhere(Aeq[:,i] == 1)
    distances = np.append(distances, NN[indexes[0], indexes[1] - 6])
    i = i + 1

Beq = np.array([1] * Aeq.shape[0])

bounds = tuple( [ (0, None) for a in range (0, Aeq.shape[1]) ] )

result = linprog(distances, A_eq = Aeq, b_eq = Beq, bounds=bounds, method="simplex")

print(result.x)
print(result.fun)

# 1 <> 3, 2 <> 6, 4 <> 5

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6])

indexes = np.argwhere(result.x == 1)
for i in indexes:
    nodes = np.argwhere(Aeq[:, i] == 1)[:, 0]
    G.add_edge(nodes[0] + 1, nodes[1] - 5)

nx.draw(G, with_labels=True)
plt.show() 
"""
A Graph G is a list of lists of tuples (adjacent, weight) of every vertex.

G = [ [(1,5), (2,-1)], [(0,1)], [(1, 5)]]
v_0 -> v_1 has weight 5
v_0 -> v_2 has weight -1

v_1 -> v_0 has weight 1

v_2 -> v_1 has weight 5

"""
import numpy as np

def BellmanFord(G, s):
	Pi = [None for v in G] # list of predecessors
	d = [np.inf for v in G] # list of distances from root s
	d[s] = 0

	for i in range(1, len(G)):
		for u, adj in enumerate(G):
			for v, w in adj:
				if (d[v] > d[u] + w):
					d[v] = d[u] + w
					Pi[v] = u


	for u, adj in enumerate(G):
			for v, w in adj:
				if (d[v] > d[u] + w):
					return (False, None, None)

	return (True, d, Pi)


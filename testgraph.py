"""
A Graph G is a list of lists of tuples (adjacent, weight) of every vertex.

G = [ [(1,5), (2,-1)], [(0,1)], [(1, 5)]]
v_0 -> v_1 has weight 5
v_0 -> v_2 has weight -1

v_1 -> v_0 has weight 1

v_2 -> v_1 has weight 5

"""
from bellman import BellmanFord

import numpy as np
import scipy.stats as stats


def find_successor(u,v, G, Pi, weight):
	if u == v:
		return weight
	else:
		x = Pi[v]
		if x == None:
			return np.inf
		# this is weight of edge (x,v)
		w = [ ww for (xx,ww) in G[x] if xx == v][0]
		# print(w)
		return find_successor(u,x, G, Pi, weight + w)


def gen_graph(graph_size, mean_number_of_adjacents=4, weight_min=-5, weight_max=5, positive=False):

	# select root
	s = np.random.choice(graph_size)
	vertexes_used = [s]
	vertexes_remaining = list(range(graph_size))
	vertexes_remaining.remove(s)

	if (weight_min < 0 and positive):
		weight_min = 0

	# Graph, List of predecessors and depth
	G = [ [] for v in range(graph_size)]
	Pi = [ None for v in range(graph_size)]
	d = [ np.inf for v in range(graph_size)]
	d[s] = 0

	while len(vertexes_remaining) > 0:
		# choose which vertex should be the parent for the next set of adjacents
		# print('used', vertexes_used, 'remaining', vertexes_remaining)
		# print(G)
		u = np.random.choice(vertexes_used)
		vertexes_used.remove(u) # will not have any further children

		p = (mean_number_of_adjacents-1)/len(vertexes_remaining)
		p = stats.binom.pmf(np.arange(len(vertexes_remaining)), len(vertexes_remaining)-1, p)
		# number of adjacents for u
		nmb_adjacents = np.random.choice(range(1,len(vertexes_remaining)+1), p=p)
		# print('adj', nmb_adjacents)
		for i in range(nmb_adjacents):
			# choose child for u
			v = np.random.choice(vertexes_remaining)
			vertexes_used.append(v)
			vertexes_remaining.remove(v)
			# choose weight for edge (u,v)
			w = np.random.randint(weight_min, weight_max+1)
			G[u].append((v, w))
			Pi[v] = u
			d[v] = d[u] + w

	
	# now generate all the other connections
	for u in range(graph_size):
		for v in range(graph_size):
			if (Pi[v] == u) or np.random.randint(2):
				continue
			weight = find_successor(u,v, G, Pi, 0)
			if weight < np.inf:
				G[u].append((v,weight+np.random.choice(range(1,4))))


	return G, s, Pi, d





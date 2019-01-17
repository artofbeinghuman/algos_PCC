"""
The graph files given by the professor are built in such a way, that if a graph contains for example 100 vertices (sommets), 
then these vertices won't be necessarily called by the index from 1 to 100, but they could also be named 3120, 412, 10, 31, 111, etc.
Thus, we'll make a list, that translates it's indices to the original vertex number (I'll call it vertex_name) from the graph file.
"""

import numpy as np


"""
if you want to later translate the names given from your algo to the names of the original graph file
set return_12v=True (return index_to_vertex_name) in the function call.
"""

def import_graph(file = "graphs/testgraphw.txt", return_i2v=False):


	# read in sommets and construct vertex_name. This way, we also get the total number of vertices
	graphfile = open(file, 'r')
	index_to_vertex_name, _, edges = graphfile.read().partition('Sommets:')[2].partition('Arcs:')
	index_to_vertex_name = np.fromstring(index_to_vertex_name.replace('\n',''), dtype=int, sep=',')

	# this will be a dictionary (avg complexity of O(1))
	vertex_name_to_index = {vertex: index for index, vertex in enumerate(index_to_vertex_name)}



	# read in edges (arcs) and start building graph
	G = list(np.zeros(len(index_to_vertex_name)))
	for line in edges.split('\n'):
		if line == '':
			# print('emptyline found')
			continue

		vertex, _, adjacents = line.partition(' : ')
		vertex = int(vertex)

		# check whether we have to read in weighted graph
		if adjacents.partition('(')[2]=='':
			adjacents = list(np.fromstring(adjacents, dtype=int, sep=','))
			# since our algos expect a weight for every arc, I assign weight 1 for the unweighted graphs
			G[vertex_name_to_index[vertex]] = [(vertex_name_to_index[adj], 1) for adj in adjacents]
		else:
			adjacents = adjacents[1:-1].split('),(')
			G[vertex_name_to_index[vertex]] = [(vertex_name_to_index[int(adj.split(', ')[0])], int(adj.split(', ')[1])) for adj in adjacents]
			

	if return_i2v:
		return G, index_to_vertex_name
	else:
		return G



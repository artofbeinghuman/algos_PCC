# Algos de PCC:


Pour tester nos algos, je suggère d'utiliser ipython ou pyzo.

Les imports:
```python
from importgraph import import_graph
import astar2
import bellman
import dijkstra
```


Puis, on importe un graphe comme ça:
```python
g, index_to_vertex_name = import_graph("graphs/CachanGraphe7.txt", True)
```

Nos algos s'attendent à ce que les sommets soient énumerés de 1 à n. Inversement, vos 
graphes ont des sommets avec une enumeration lacunaire (certains sommets entre 1 et n n'existent pas),
alors nous traduisons pendant l'import l'enumeration des sommets vers [1 .. n].
Avec index_to_vertex_name, on peut traduire les noms des sommets resultant de 
nos algos à leur nom d'origine dans votre graphe. Ça veut dire, si `s` est un 
certain sommet dans le resultat de Bellman-Ford par exemple, alors
`index_to_vertex_name[s]` donne le nom originel de ce sommet.


Pour tester l'algo Bellman-Ford, lancez:
```python
s = 10 # choisir un sommet de début
success, dist, Pi = bellman.BellmanFord(g, s) # dist=les distances, Pi=les prédecesseurs
```

Pour tester l'algo A*, lancez:
```python
s = 10 # choisir un sommet de début
t = 0 # choisir un sommet de cible
dist, Pi = astar2.Astar(g, s, t)
```


Pour tester l'algo de Dijkstra, lancez:
```python
s = 10 # choisir un sommet de début
dist, Pi = dijkstra.Dijkstra(g, s)
```

Pour tester les files de Fibonacci, se référer au fichier fibonacci.py

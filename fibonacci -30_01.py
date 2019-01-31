"""
This file showcases an implementation of Fibonacci heaps in objective Python.
Those are Fibonacci heaps that were described by Serge Haddad in the 2018 Algorithmics course.

An Entry is a class with two fields : 
	- ent.key, the key, used to sort (could be an integer or infinity, for instance)
	- ent.val, the value, which will be used by further algorithms.

A Fibonacci Heap (class Fibo), is a class with two fields:
	- fib.t, the dictionary of turnament trees, whose nodes are coloured dynamically
	- fib.p, a pointer to the smallest root

A Tree is a class with two fields:
	- arb.r, the root of the tree
	- arb.v, the list of the pointers to the child trees

A graph is an adjacency list, with |S| lists of couples (destination,weight).
[[(2,0)],
[(0,4),(2,17)],
[(3,-1)],
[]]


Operations on Fibonacci Heaps :

insert		DONE
accessmin	DONE
deletemin
decreasekey	DONE
delete		
merge		DONE

Copyright (c) 2018, Ulysse REMOND
"""

"""False for easy tests, True for hard"""
hard = True


#from inflib import *
from numpy import inf

class Entry:
	""" tentative d'implémentation des pointeurs en Python"""
	def __init__(self,key,value):
		self.key = key
		self.val = value
	def __repr__(self):
		return("key :"+ str(self.key) + ", value: " + str(self.val))

class Tree:
	"""
	Classe représentant un arbre (i.e. un somme d'un arbre)
	r: valeur du sommet
	v: Liste d'Arbres fils
	f: père du sommet(cas où il est inclus); None, le cas échéant
	m: booléen indiquant si on est marqué ou non
	"""
	def __init__(self,node):
		""" initial node, which is of type ref(Entry) """
		self.r = node
		self.v = []
		self.f = None
		self.m = False#is unmarked by default -will be marked with decreasekey
	
	def degre(self):
		"""number of children of the tree: O(1)"""
		return len(self.v)
		
	def fusionArbres(self,tree):
		"""Basic tree fusion, with the lowest key put atop of the tree: O(1)"""
		
		if tree.r.obj.key < self.r.obj.key:
			#tree va etre le pere de self
			newtree = tree
			newtree.v.append(ref(self))
			self.f = tree
			return newtree
		else:
			newtree = self
			newtree.v.append(ref(tree))
			tree.f = newtree
			return newtree
			
	def __repr__(self):
		"""0 means unmarked. The list of the subtrees is between brackets"""
		return ("\n"+str(int(self.m))+"Tree:"+str(self.r.obj)+"("+str(self.v)+")")
		
class ref:
	""" Simulation de pointeurs 
	ref(obj) crée un pointeur vers obj
	"""
	def __init__(self, obj):
		self.obj = obj#creates a new pointer to the object obj
	def get(self):
		return self.obj#returns the value
	def set(self, new_obj):
		self.obj = new_obj#sets the value of the pointee to new_obj
	def __repr__(self):
		return str(self.obj)

class Fibo:
	"""
	t: Dictionnaire d'arbres tournois, aux noeuds colorés dynamiquement
	p: Pointeur sur le minimum
	"""
	def __init__(self,value,maketree=True):
		"""O(1) initializes the heap"""
		if maketree:
			self.t = [Tree(value)]
		else:#it is already a tree
			self.t = [value]
		self.p = 0
	def empty(self):
		return self.t == []
	def accessmin(self):
		"""O(1) returns the value of the heap paired with the minimal key"""
		if self.empty():
			print("Empty heap")
			return inf
		return self.t[self.p].r.obj.val
	
	
	def minimalkey(self):
		"""O(1) returns the minimal key of the heap"""
		if self.empty():
			print("Empty heap")
			return inf
		return self.t[self.p].r.obj.key
		
	def insert(self,value):
		"""O(1) inserts an Entry "ent" into the heap  """
		if self.empty():#empty heap
			self.__init__()
		else:
			mini = self.minimalkey() #this is the min of the heap
		
			if mini > value.obj.key :
				self.p = len(self.t) #the new element is the smallest
			self.t.append(Tree(value))# adding a list of one tree with only one node
	
	def merge(self,feap):
		"""O(1) merges the heap with another Fibonacci heap named feap"""
		mini = self.minimalkey()#this is the min of the heap
		minf = feap.minimalkey()#This is the min of feap
		if mini > minf :
			self.p = len(self.t) + feap.p#changing minimum
		self.t += feap.t             #merging feap 

	def decreasekey(self,ref_ent,new_key):
		"""O(1) decreases the key of the root of the tree ref_ent """

		ent = ref_ent.r.obj
		if ent.key < new_key:
			print("You are trying to increase a key ! Only decreases are permitted.")
			return -1
		
		if ref_ent.f != None:#it is not the root
			father = ref_ent.f# TODO see the section : "Remarques importantes"
			if father.r.obj.key > new_key:#father has bigger key
				father.v.remove(ref_ent)#severing the child tree
				self.merge(Fibo(ref_ent))#the new p is computed here
				self.t[len(self.t)-1].m = False#ref_ent becomes an unmarked root
				
				if father.f != None:#father is not a root
					if father.m:
						self.decreasekey(ref_ent.f,father.key)#decrease coloured father
					else:
						ref_ent.f.m = True#coloring the father
						#ref_ent.f.r.set(father) faudra t'il utiliser ça?
			else:
					#father's key is smaller => p, f are unchanged. 
				pass
		ent.key = new_key#setting the key
		ref_ent.r.set(ent)
		
	def deletemin(self):
		"""deletes the minimal value O(log(n))"""
		ancien_p = self.p#ancienne valeur du minimum
		minimal_tree = self.t[self.p]
		
		ajout_fils = 0
		for tree_pointer in minimal_tree.v:
			print("Fusion de " + str(tree_pointer.obj.r) + " et de ses fils")
			#ajout des fils directement dans la liste
			# tree_pointer est un pointeur vers un arbre -> d'où le False
			self.merge(Fibo(tree_pointer.obj,False))
			

			if tree_pointer.obj.r.obj.key < self.minimalkey() :
				self.p = ajout_fils
			ajout_fils += 1
		print("Suppressing the value "+str(self.t[self.p].r.obj.val))
		del self.t[ancien_p]#suppression du minimum
		
		#compactage de la liste
		pointers = dict()#tableau des (pointeurs,indice) , indicé par degré
		
		arbre_supp = 0
		for tree_indice in range(len(self.t)):
			print(tree_indice,arbre_supp,tree_indice-arbre_supp,self.p)
			tree_indice -= arbre_supp
			print("Testing the value " + str(self.t[tree_indice].r) + "<? "+ str(self.minimalkey()))
			#invariant : on ne peut supprimer que des arbres déja ajoutés
			ok = False
			while not ok:
				ok = True
				tree = self.t[tree_indice]
				deg = tree.degre()#la mesure du degré se fait en temps constant
				if not deg in pointers:
					#il n'existe pas de degré identique
					pointers[deg] = (ref(tree),tree_indice)
					if tree.r.obj.key < self.minimalkey() :
						print("!!!!!!!!!!!!!"+str(self.t[tree_indice].r))
						self.p = tree_indice
				else:
					self.t[tree_indice] = tree.fusionArbres(pointers[deg][0].obj)
					
					#supprime dans self l'arbre d'indice pointers[deg][1]
					del self.t[pointers[deg][1]]
					if pointers[deg][1] < self.p:
						self.p -=1 
					arbre_supp += 1
					tree_indice -= 1
					if tree.r.obj.key < self.minimalkey() :
						self.p = tree_indice
					
					#pointers[deg] a disparu de Fibo
					del pointers[deg]
					ok = False
			
	def delete(self,ref_ent):
		"""deletes the values which is pointed by ref_ent, in O(log(n))"""
		decreasekey(self,ref_ent,(-inf))
		#it is now the minimal value,as nothing is less than (-inf)
		deletemin(self)
		
	def __repr__(self):
		""" used to print the Fibonacci heap"""
		return ("t :"+ str(self.t) + "\np: " + str(self.p))



""" test section """
s1 = Entry(100,1)
r1 = ref(s1)
s2 = Entry(150,2)
r2 = ref(s2)
blop = Fibo(r1)
s3 = Entry(60,3)
r3 = ref(s3)
s6 = Entry(600,6)
r6 = ref(s6)
blop.insert(r6)
s7 = Entry(700,7)
r7 = ref(s7)
blop.insert(r7)
s8 = Entry(800,8)
r8 = ref(s8)
blop.insert(r8)
blop.insert(r3)
blop.insert(r2)
#print(blop)
s4 = Entry(400,4)
r4 = ref(s4)
blop.insert(r4)
s5 = Entry(500,5)
r5 = ref(s5)
blop.insert(r5)

blop.decreasekey(blop.t[blop.p],48)
blop.decreasekey(blop.t[-1],42)
#print(blop)
"""test du pointeur"""
s5.key = 499
#print(blop)
blop.decreasekey(blop.t[-5],497)
print(blop)
print("s5 = ",s5)
if hard:
	T = [-1 for _ in range(1001)]
	S = [-1 for _ in range(1001)]
	for t in range(9,1001):
		S[t] = Entry(44449*44417*t % 1100,t)
		T[t] = ref(S[t])
		blop.insert(T[t])

"""tests de deletemin(
blop.deletemin()
blop.t[0].v[1].v[0].f.f
"""

"""
Remarques importantes:

# ligne 115:
ref_ent est un arbre dont les noeuds sont des Ref (Entry)
ref_ent.r est une reférence vers une entrée
ref_ent.r.obj est une entrée
ref_ent.r.obj.val est un entier (valeur)
ref_ent.r.obj.key est un entier (clef)
ref_ent.f est un arbre, ou None
ref_ent.f.r.obj.key est un entier (clef)
self.t[self.p].r.obj.key est un entier
"""
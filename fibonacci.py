"""
This file showcases an implementation of Fibonacci heaps in objective Python.
Those are Fibonacci heaps that were described by Serge Haddad in the 2018 Algorithmics course.

An Entry is a class with two fields : 
	- ent.key, the key, used to sort (could be an integer or infinity, for instance)
	- ent.val, the value, which will be used by further algorithms.

A Fibonacci Heap (class Fibo), is a class with two fields:
	- fib.t, the circular list of turnament trees, whose nodes are coloured dynamically
	- fib.p, a pointer to the smallest root

A Tree is a class with two fields:
	- arb.r, the root of the tree
	- arb.v, the list of the child trees

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
from inflib import *
from numpy import inf

class Tree:
	"""
	r: valeur du sommet
	v: Liste d'Arbres fils
	f: père du sommet(cas où il est inclus); None, le cas échéant
	m: booléen indiquant si on est marqué ou non
	"""
	def __init__(self,value):
		""" initial value """
		self.r = value
		self.v = []
		self.f = None
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

class Fibo:
	"""
	t: Liste cirulaire d'arbres tournois, aux noeuds colorés dynamiquement
	p: Pointeur sur le minimum
	"""
	def __init__(self,value):
		"""O(1) initializes the heap"""
		self.t = [Tree(value)]
		self.p = 0

	def accessmin(self):
		"""O(1) returns the minimal value of the heap"""
		return self.t[self.p].r.key

	def insert(self,ent):
		"""O(1) inserts an Entry "ent" into the heap  """"
		mini = accessmin(self) #this is the min of the heap
	
		if mini > ent.key :
			self.p = len(self.t) #the new element is the smallest
		self.t.append([ent])# adding a list of one tree with only one node
	
	def merge(self,feap):
		"""O(1) merges the heap with another Fibonacci heap named feap"""
		mini = accessmin(self)#this is the min of the heap
		minf = accessmin(self)#this is the min of feap
		if mini > minf :
			self.p = len(self.t) + feap.p#changing minimum
		self.t += feap.t             #merging feap 

	def decreasekey(self,ref_ent,new_key):
		"""O(1) decreases the key of the Entry whose values matches ent.val """
		ent = ref_ent.obj.get()
		if ent.r.key < new_key:
			print("You are trying to increase a key ! Only decreases are permitted.")
			return -1
		ent.r.key = new_key#setting the key
		"""ref_ent.obj.set(ent)                               this line should be useless"""
		if ent.f != None:#it is not the root
			father = ent.f.obj.get()
			if father.f != None:#father is not a root
				if father.m:
					self.decreasekey(ent.f.obj,father.key)#decrease coloured father
				else:
					father.m = True#coloring the father
					ent.f.obj.set(father)
		ref_ent.obj.set(ent)
		
		
	def deletemin(self):
		"""deletes the minimal value"""
		minimal_tree = self.t[self.p].r
		for tree_pointer in minimal_tree.v:
			tree = tree_pointer.get()
			merge(self,Fibo())
		self.t = self.t[:self.p] + self.t[(self.p+1):]
		
		#compactage de la liste
		pointers = []#tableau des pointeurs, indicé par degré
		for tree in self.t:
			pass# TODO POINTERS !!!!

	def delete(self,ref_ent):
		"""deletes the values which is pointed by ref_ent"""
		decreasekey(self,ref_ent,(-inf))
		#it is now the minimal value
		deletemin(self)
		
	def __repr__(self):
		""" used to print the Fibonacci heap"""
		print("t :"+ str(self.t) + "\np: " + str(self.p))


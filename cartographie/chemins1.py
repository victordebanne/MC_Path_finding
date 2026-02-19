#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Algorithme pour trouver des chemins 
On chercher les extremités du champs de vision d'un point et on 
construit un arbre à partir ça. 
chaque point à l'extremité construit son champs de vision jusqu'a trouver
le point d'arrivée
"""
from visionpath import Space, matrixify
from islandes import random_islande
import matplotlib.pyplot as plt
import random as r
import time


#-----ALGEBRE UTILES-----
def vect(A, B):
    return [B[0] - A[0],B[1] - A[1]]

def norm(v):
    return (v[0]**2 + v[1]**2)**0.5

def mult(v, k):
    return [v[0] * k, v[1] * k]

def add(u, v):
    return [v[0] + u[0], v[1] + u[1]]

def produit_vectoriel(u, v):
    return u[0] * v[1] - u[1] * v[0] 

def create_matrix(i, j):
    return [[0 for k in range(j)]for k in range(i)]

def dist(u, v):
    return ((v[0] - u[0])**2 + (v[1] - u[1])**2)**0.5



#-----INITIALISATION-----

#matrix est la carte sur laquelle on souhate se déplacer
#A est le départ 
#B est l'arrivée

#out est la matrice sur laquelle on fait nos opérations
#les Nodes sont les noeuds possibles de passage 
#on marque les champs de vision avec des 1 puis on les remplaces avec des Nodes
#on marque les cases vues par des 0.5 et on garde les cases extremes en Nodes
#les cases 0 sont les cases inexplorées
#dans la matrice out, les murs sont données par un 2

A = [40, 10]
B = [10, 40]
M = None
"""
while True : 
    #créé un espace avec A et B libres
    S = Space(5)
    M = matrixify(S, 50, 50)
    if M[A[0]][A[1]] == 0 and M[B[0]][B[1]] == 0 : 
        break
"""
while True : 
    #créé un espace avec A et B libres
    M = create_matrix(50, 50)
    random_islande(M, 40, 7, 0.7)
    if M[A[0]][A[1]] == 0 and M[B[0]][B[1]] == 0 : 
        break
    
    
ops = 0    
    
#-----ALGORITHME-----

def line(out, matrix, A, B):
    out[A[0]][A[1]] = 2
    out[B[0]][B[1]] = 2
    AB = vect(A, B)
    depart = A
    position = A
    
    k = int(AB[0]/abs(AB[0])) if AB[0] != 0 else 0
    l = int(AB[1]/abs(AB[1])) if AB[1] != 0 else 0

    
    while True : 
        out[A[0]][A[1]] = 2
        out[B[0]][B[1]] = 2
        global ops
        ops += 1
        
        a = [position[0], position[1] + l]
        b = [position[0] + k, position[1] + l]
        va = vect(depart, a)
        vb = vect(depart, b)
        p = produit_vectoriel(AB, va) * produit_vectoriel(AB, vb)
        if p < 0 : 
            position = add(position, [0, l])
        elif p == 0 :
            position = add(position, [k, l])
        else : 
            position = add(position, [k, 0])
            
        out[position[0]][position[1]] = 1
        
        if position == B : 
            break

def line_test(out, matrix, A, B):

    AB = vect(A, B)
    depart = A
    position = A
    
    k = int(AB[0]/abs(AB[0])) if AB[0] != 0 else 0
    l = int(AB[1]/abs(AB[1])) if AB[1] != 0 else 0

    
    while True : 
        if position == B : 
            return 0
        
        global ops
        ops += 1

        a = [position[0], position[1] + l]
        b = [position[0] + k, position[1] + l]
        va = vect(depart, a)
        vb = vect(depart, b)
        p = produit_vectoriel(AB, va) * produit_vectoriel(AB, vb)
        if p < 0 : 
            position = add(position, [0, l])
        elif p == 0 :
            position = add(position, [k, l])
        else : 
            position = add(position, [k, 0])
            
        if matrix[position[0]][position[1]] == 1:
            return 1
            
        out[position[0]][position[1]] = 1
        
class Node():
    def __init__(self, position, goal):
        self.position = position
        self.goal = goal
        self.possible_nodes = None
        self.temp = None
        self.path = []
        self.node = None
        self.parent = None
        self.bad = []
        self.gen = 0
        self.memoire_des_ancetres = None
        self.visited = False
        
        
    def draw_vision(self, matrix):
        if self.visited:
            return 
        #on trace le champ de vision du node en parcourant parcourant chaque point externe de la matrice
        #l'algorithme line_test regarde TOUTES les cases traversées par le segment AB, cela nous permet 
        #non pas comme Bresenham de s'assurer de marquer TOUTES les cases vues par le node.
        mi = len(matrix)
        mj = len(matrix[0])
        self.temp = create_matrix(mi, mj)
        for i in range(mi):
            for j in range(mj):
                if matrix[i][j] == 1 : 
                    self.temp[i][j] = 2
                    
        self.temp[self.position[0]][self.position[1]] = 1
                    
        for i in range(len(matrix)):
            line_test(self.temp, matrix, self.position, [i, 0])
        for i in range(1, len(matrix)):
            line_test(self.temp, matrix, self.position, [len(matrix) - 1, i])
        for i in range(1, len(matrix)):
            line_test(self.temp, matrix, self.position, [len(matrix) - 1 - i, len(matrix[0]) - 1])
        for i in range(1, len(matrix) - 1):
            line_test(self.temp, matrix, self.position, [0, len(matrix[0]) - 1 - i])
        
            
    def display_vision(self):
        plt.imshow(self.temp)
        plt.show()
        
    def borders(self):
        if self.visited :
            return 0
        self.possible_nodes = []
        mi = len(self.temp)
        mj = len(self.temp[0])
        for i in range(mi):
            for j in range(mj):
                global ops
                ops += 1
                if self.temp[i][j] == 1:
                    if [i,j] == self.goal:
                        self.path.append(self.position)
                        self.path.append(self.goal)
                        return 1
                    if self.temp[min(mi - 1, i+1)][j] == 0 or self.temp[max(0, i-1)][j] == 0 or self.temp[i][min(mj - 1, j + 1)] == 0 or self.temp[i][max(0, j - 1)] == 0 : 
                        self.possible_nodes.append([i,j])
        self.visited = True
        return 0
                
    def closest_to_goal(self):
        closest = None
        closest_dist = None
        
        for i in range(0, len(self.possible_nodes)):
            global ops 
            ops += 1
            possible = self.possible_nodes[i]
            if possible in self.path or possible in self.bad : 
                continue
            elif closest == None : 
                closest = possible
                closest_dist = dist(self.goal, possible)
            else : 
                new_dist = dist(self.goal, self.possible_nodes[i])
                if new_dist < closest_dist : 
                    closest_dist = new_dist
                    closest = self.possible_nodes[i]
            
        if closest == None : 
            self.bad.append(self.position)
            if self.parent != None : 
                self.parent.bad = [self.bad[i] for i in range(len(self.bad))]
                return 0
            else : 
                return -1
                
        self.path.append(self.position)
        new_node = Node(closest, self.goal)
        new_node.path = [self.path[i] for i in range(len(self.path))]
        new_node.bad = [self.bad[i] for i in range(len(self.bad))]
        new_node.parent = self
        new_node.gen = self.gen + 1
        self.node = new_node
        #if self.gen > 0 :
        new_node.memoire_des_ancetres = [[self.memoire_des_ancetres[i][j] for j in range(len(self.memoire_des_ancetres[0]))] for i in range(len(self.memoire_des_ancetres))]
        
        
        return 1
    
    def is_good_child(self):
        is_good = False
        for i in range(len(self.temp)):
            for j in range(len(self.temp[0])):
                global ops 
                ops += 1
                if self.memoire_des_ancetres[i][j] ==  0 and self.temp[i][j] == 1 : 
                    self.memoire_des_ancetres[i][j] = 1
                    is_good = True
                    
        return is_good
                
        
    def draw_path(self, matrix):
        out = create_matrix(len(matrix), len(matrix[0]))
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                global ops 
                ops += 1
                if matrix[i][j] == 1 : 
                    out[i][j] = 2
        for i in range(1, len(self.path)):
            
            line(out, matrix, self.path[i - 1], self.path[i])
            
        plt.imshow(out)
        plt.show()
        
    def optmisation(self):
        pass
    def function(self, matrix):
        bad = False
        print(self.gen)
        self.draw_vision(matrix)
        
        if self.gen == 0 : 
            self.memoire_des_ancetres = [[self.temp[i][j] for j in range(len(self.temp[0]))] for i in range(len(self.temp))]
            
        else : 
           
            if not self.is_good_child() : 
                print("memoire des ancètres")
                self.bad.append(self.position)
                if self.parent != None : 
                    self.parent.bad = [self.bad[i] for i in range(len(self.bad))]
                    #self.parent.function(matrix)
                    bad = True
                else : 
                    print("aucun chemin trouvé")

                    return 
                
            
        end = self.borders()
        #self.temp[self.possible_nodes[0][0]][self.possible_nodes[0][1]] = 2
        #self.display_vision()
        #time.sleep(0.3)
        if end : 
            print("chemin trouvé")
            self.chemin = 1
            self.draw_path(matrix)
            return
        else : 
            if bad : 
                self.parent.function(matrix)
            else : 
                #print(self.gen)
                close = self.closest_to_goal()
                if close == 0 : 
                    self.parent.function(matrix)
                elif close == 1 : 
                    self.node.function(matrix)
                elif close == -1 : 
                    print("aucun chemin trouvé")
                    self.chemin = -1
                    return 
                
            
plt.imshow(M) 
plt.show()
        
N = Node(A, B)

N.function(M)

    


print(ops)

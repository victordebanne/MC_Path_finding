#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chemins Monte Carlo
"""
from visionpath import Space, matrixify
import matplotlib.pyplot as plt
import random as r


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

#-----INIT-----


A = [40, 10]
B = [10, 40]

while True : 
    #créé un espace avec A et B libres
    S = Space(5)
    M = matrixify(S, 50, 50)
    if M[A[0]][A[1]] == 0 and M[B[0]][B[1]] == 0 : 
        break
    
plt.imshow(M)
plt.show()

def line_test(matrix, A, B):
    AB = vect(A, B)
    depart = A
    position = A
    
    k = int(AB[0]/abs(AB[0])) if AB[0] != 0 else 0
    l = int(AB[1]/abs(AB[1])) if AB[1] != 0 else 0

    
    while True : 
        if position == B : 
            return 1
        


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
            return 0


class Node():
    def __init__(self, position):
        self.position = position
        self.degreA = 10000 
        self.degreB = 10000
        
        self.distA = 10000
        self.distB = 10000
        
        self.total = 20000
        
        
        self.links = []
        self.dists = []


            
        
        
class Simulation():
    def __init__(self, size, matrix):
        self.size = size
        self.mi = len(matrix)
        self.mj = len(matrix[0])
        self.nodes = []

        for i in range(self.size):
            x = r.randint(0, self.mi - 1)
            y = r.randint(0, self.mj - 1)
            self.nodes.append(Node([x,y]))
            
    def watching(self, matrix, Dep, Arr):
        #watching créé un graph de visibilité
        for i in range(self.size):
            #vois le départ
            if line_test(matrix, self.nodes[i].position, Dep):
                self.nodes[i].degreA = 1
                self.nodes[i].distA = dist(self.nodes[i].position, Dep)
                
            #vois l'arrivée
            if line_test(matrix, self.nodes[i].position, Arr):
                self.nodes[i].degreB = 1
                self.nodes[i].distB = dist(self.nodes[i].position, Arr)
                
            #on regarde seulement les binomes uniques
            for j in range(i + 1, self.size):
                if line_test(matrix, self.nodes[i].position, self.nodes[j].position):
                    #connexion bilaterale
                    distance = dist(self.nodes[i].position, self.nodes[j].position)
                    self.nodes[i].links.append(self.nodes[j])
                    self.nodes[i].dists.append(distance)
                    self.nodes[j].links.append(self.nodes[i])
                    self.nodes[j].dists.append(distance)
                    
    def find_path(self):
        #le plus simple serait un dijkstra
        #mais je tente autre chose 
        
        for i in range(self.size):
            for j in range(len(self.nodes[i].links)):
                node = self.nodes[i].links[j]
                distanceA = node.distA + self.nodes[i].dists[j]
                if distanceA < self.nodes[i].distA : 
                    self.nodes[i].distA = distanceA
                    
                elif distanceA > self.nodes[i].distA : 
                    node.distA = self.nodes[i].distA + self.nodes[i].dists[j]
                    
                    
                distanceB = node.distB + self.nodes[i].dists[j]
                if distanceB < self.nodes[i].distB : 
                    self.nodes[i].distB = distanceB
                    
                elif distanceB > self.nodes[i].distB : 
                    node.distB = self.nodes[i].distB + self.nodes[i].dists[j]
                    
            self.nodes[i].total = self.nodes[i].distA + self.nodes[i].distB

    def find(self):
        index = None
        for i in range(self.size):
            node = self.nodes[i]
            if node.degreA == 1 :
                if index == None :
                    index = i
                else : 
                    if self.nodes[index].total > self.nodes[i].total:
                        index = i
        
        
        best_node = self.nodes[index]
        # on pourrait ici reconstruire un chemin vers B
        # en suivant toujours le voisin avec distB minimal
        path = [best_node.position]
        current = best_node
        while current.degreB != 1:
            # choisir le lien avec distB minimal
            next_node = min(current.links, key=lambda n: n.distB)
            if next_node.position in path:
                break  # boucle
            path.append(next_node.position)
            current = next_node
        path.append(B)
        
        
        return path
            
                    
                
            
    def display(self):
        for i in range(self.size):
            plt.scatter(self.nodes[i].position[1], - self.nodes[i].position[0])
        plt.xlim(0, 50)
        plt.ylim(-50, 0)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
        
    def display_graph(self):
        for i in range(self.size):
            for j in range(len(self.nodes[i].links)):
                x1 = self.nodes[i].position[1]
                x2 = self.nodes[i].links[j].position[1]
                y1 = -self.nodes[i].position[0]
                y2 = -self.nodes[i].links[j].position[0]
                x = [x1, x2]
                y = [y1, y2]
                plt.plot(x, y)
        plt.xlim(0, 50)
        plt.ylim(-50, 0)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
        plt.show()
              
              
S = Simulation(200, M)
for i in range(1):
    S.watching(M, A, B)
    S.find_path()
    S.find_path()
    S.find_path()

    #S.display()
    S.display_graph()
    #S.resampling()
    
path = S.find()
path.insert(0,A)
print(path)

for i in range(len(path) - 1):
    x1 = path[i][1]
    x2 = path[i + 1][1]
    y1 = -path[i][0]
    y2 = -path[i + 1][0]
    x = [x1, x2]
    y = [y1, y2]
    plt.plot(x, y)
plt.xlim(0, 50)
plt.ylim(-50, 0)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
plt.show()





                        
            
        
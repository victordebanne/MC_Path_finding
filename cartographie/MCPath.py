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
        

            
        
        
class Simulation():
    def __init__(self, size, matrix):
        self.size = size
        self.mi = len(matrix)
        self.mj = len(matrix[0])
        self.nodes = []
        self.proba = [1/(self.size) for i in range(self.size)]
        for i in range(self.size):
            x = r.randint(0, self.mi - 1)
            y = r.randint(0, self.mj - 1)
            self.nodes.append(Node([x,y]))
            
        self.resample = [None for i in range(self.size)]

            
    def watching(self, matrix, Dep, Arr):
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
                #si les points se voient 
                if line_test(matrix, self.nodes[i].position, self.nodes[j].position):
                    #pour A : 
                    #si i > j alors degreA de j = degreA de i + 1
                    #sinon inférieru, l'iverse, sinon on ne fait rien
                    if self.nodes[i].degreA < self.nodes[j].degreA :
                        self.nodes[j].degreA = self.nodes[i].degreA + 1
                    distance = dist(self.nodes[j].position, self.nodes[i].position) + self.nodes[i].distA
                    if distance < self.nodes[j].distA : 
                        self.nodes[j].distA = distance
                            
                    elif self.nodes[i].degreA > self.nodes[j].degreA : 
                        self.nodes[i].degreA = self.nodes[j].degreA + 1
                    distance = dist(self.nodes[j].position, self.nodes[i].position) + self.nodes[j].distA
                    if distance < self.nodes[i].distA : 
                        self.nodes[i].distA = distance
                    
                    #pour B : 
                    if self.nodes[i].degreB < self.nodes[j].degreB :
                        self.nodes[j].degreB = self.nodes[i].degreB + 1
                    distance = dist(self.nodes[j].position, self.nodes[i].position) + self.nodes[i].distB
                    if distance < self.nodes[j].distB : 
                        self.nodes[j].distB = distance
                            
                    elif self.nodes[i].degreB > self.nodes[j].degreB : 
                        self.nodes[i].degreB = self.nodes[j].degreB + 1
                    distance = dist(self.nodes[j].position, self.nodes[i].position) + self.nodes[j].distB
                    if distance < self.nodes[i].distB : 
                        self.nodes[i].distB = distance
                        
   
    def compute_proba(self):
        #on calcule les probabilités à partir du deuxième tour
        total = 0
        for i in range(self.size):
            self.proba[i] += (1/(self.nodes[i].degreA * self.nodes[i].degreB)**2) + (1/(self.nodes[i].distA * self.nodes[i].distB + 0.1)**2)
            total += self.proba[i]
            
        #normalisation
        for i in range(self.size):
            self.proba[i] /= total
            
    def search(self):
        #on cherche le point de plus petit degré et de plus petite distance. 
        smallest = (self.nodes[0].distA + self.nodes[0].distB) *  (self.nodes[0].degreA + self.nodes[0].degreB)
        index = 0
        for i in range(1, self.size):
            test = (self.nodes[i].distA + self.nodes[i].distB) *  (self.nodes[i].degreA + self.nodes[i].degreB)
            if test < smallest :
                smallest = test 
                index = i
                
        return self.nodes[index].distA, self.nodes[index].distB, self.nodes[index].degreA, self.nodes[index].degreB, self.nodes[index].position
                

    def display(self):
        for i in range(self.size):
            plt.scatter(self.nodes[i].position[1], - self.nodes[i].position[0], s = self.proba[i] * 1000)
        plt.show()
                            
S = Simulation(100, M)
for i in range(1):
    S.watching(M, A, B)
    S.compute_proba()
    S.display()
    #S.resampling()
    
print(S.search())



                        
            
        
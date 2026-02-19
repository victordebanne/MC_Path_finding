#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Champs de forces pour exploration vers l'inconnu
"""

import matplotlib.pyplot as plt
import time 
import random as r

def create_matrix(i, j):
    return [[0 for k in range(j)] for k in range(i)]

def vect(a, b):
    return [b[0] - a[0], b[1] - a[1]]

def norm(v):
    return (v[0]**2 + v[1]**2)**0.5

def normalize(v):
    return [v[0] / norm(v), v[1] / norm(v)]

def rotate(v, sens = 1):
    return [-v[1] * sens, v[0] * sens]

def mult(v, k):
    return [v[0] * k, v[1] * k]

def add(u, v):
    return [u[0] + v[0], u[1] + v[1]]


M = create_matrix(100, 150)
M[45][45] = 2
M[30][45] = 2
M[20][70] = 2

agent = [25, 25]
vitesse = [0, 0]



def vectorfield(matrix, agent):
    vector = [0, 0]
    K = [0, 0, -10]
    C = [1, 1, 1]
    
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            
            r = vect([i,j], agent)
            d = norm(r)
            
            k = None
            for l in range(len(K)):
                if matrix[i][j] == l:
                    #C[l] +=1
                    k = K[l] / C[l]
                
                    
            e = 0.1
            
            f = mult(r, k/(d**2 + e))
            
            vector[0] += f[0]
            vector[1] += f[1]
 
    return vector

for i in range(5000):
    if agent[0] >= 99 or agent[0] <= 0:
        agent[0] = 25
    if agent[1] >= 99 or agent[1] <= 0:
        agent[1] = 25

    M[int(agent[0])][int(agent[1])] = 1
    
    vitesse = add(vitesse, mult(vectorfield(M, agent), 0.01))
    vitesse[0] = min(5, vitesse[0])
    vitesse[1] = min(5, vitesse[1])

    agent = add(agent,vitesse)
    
    plt.imshow(M)
    plt.show()


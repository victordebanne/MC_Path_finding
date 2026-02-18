#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 17:34:25 2026

@author: victordebanne
"""
from algebra import create_matrix
from islandes import random_islande
from pathfinding import path_finding

def create_map(size_i, size_j, A, B):
    global M
    while True : 
        #créé un espace avec A et B libres
        M = create_matrix(size_i, size_j)
        random_islande(M, 40, 7, 0.7)
        if M[A[0]][A[1]] == 0 and M[B[0]][B[1]] == 0 : 
            break
        
M = None
A = [40, 10]
B = [10, 40]        
        
create_map(50, 50, A, B)


print(path_finding(100, M, A, B))

        

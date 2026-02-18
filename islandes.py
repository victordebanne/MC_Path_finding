#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 16:35:39 2026

@author: victordebanne
"""
import random as r
import matplotlib.pyplot as plt

def create_matrix(i,j):
    return [[0 for k in range(j)]for k in range(i)]

M = create_matrix(50, 50)

def random_islande(matrix, nb, size, proba):
    for k in range(nb):
        i = r.randint(0, len(matrix) - 1)
        j = r.randint(0, len(matrix[0]) - 1)
        
        matrix[i][j] = 1
    islandise(matrix, size, proba)
        
def islandise(matrix, size, proba):
    if size == 0 : 
        return 
    temp = create_matrix(len(matrix), len(matrix[0]))
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            temp[i][j] = matrix[i][j]
            
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[0]) - 1):
            if matrix[i+1][j] == 1 or matrix[i-1][j] == 1 or matrix[i][j + 1] == 1 or matrix[i][j-1] == 1:
                alpha = r.random()
                if alpha > proba:
                    temp[i][j] = 1
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = temp[i][j]       
    islandise(matrix, size - 1, proba)
        
    

    

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MATRIX and VECTOR UTILITIES
"""


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

def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]
           
def proj(u, v):
    k = dot(u, v) / norm(v)**2
    return [v[0] * k, v[1] * k]

def rebond(u, v):
    #la formule 2 * proj(u sur v) - u est equivalent au rebond par rapport à la normale
    return add(mult(u, -1), mult(proj(u, v), 2))
        
def mirror(matrix):
    out = [[0 for i in range(len(matrix[0]))] for i in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            out[i][j] = matrix[len(matrix) - 1 - i][j]
    return out
            

                






        
        
        

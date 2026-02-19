
"""
Created on Tue Jan 20 17:16:50 2026

@author: victordebanne
"""

import matplotlib.pyplot as plt
import random as r

def vect(A, B):
    return [B[0] - A[0],B[1] - A[1]]

def norm(v):
    return (v[0]**2 + v[1]**2)**0.5

def mult(v, k):
    return [v[0] * k, v[1] * k]

def add(u, v):
    return [v[0] + u[0], v[1] + u[1]]

def creat_matrix(i, j):
    return [[0 for k in range(j)] for k in range(i)]

def random_noise(matrix):
    x = r.randint(0, 99)
    y = r.randint(0, 99)
    matrix[x][y] = 1
    
def produit_vectoriel(u, v):
    return u[0] * v[1] - u[1] * v[0] 

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
        
        if matrix[position[0]][position[1]] == 1:
            return 1
        
        if position == B : 
            return 0

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
        
            
        
            
     
        
        

    
if __name__ == "__main__" : 
    M = creat_matrix(100, 100)
    O = creat_matrix(100, 100)
    A = [r.randint(0, 99), r.randint(0, 99)]
    B= [r.randint(0, 99), r.randint(0, 99)]
    
    print(A, B)
    
    line(O, M, A, B)
    plt.imshow(O)
    plt.show()


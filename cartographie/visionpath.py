#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VISION BASED PATH FINDER
"""
import matplotlib.pyplot as plt
import time
import random as r
from ALG import create_matrix, vect, norm, normalize, rotate, mult, add, dot, proj,rebond, mirror

def hitbox(a, b, w = 1):
    ab = vect(a, b)
    bc = mult(rotate(normalize(ab)), w)
    A = add(a, mult(bc, -1/2))
    B = add(A, ab)
    C = add(B, bc)
    D = add(C, mult(ab, -1))
    
    return [A, B, C, D]
    
def display_poly(poly):
    for i in range(len(poly)):
        plt.plot([poly[i - 1][0], poly[i][0]], [poly[i - 1][1], poly[i][1]])
  
def is_in_poly(a, poly):
    for i in range(len(poly)):
        d = dot(vect(poly[i - 1], a), vect(poly[i-1], poly[i]))
        if d < 0 : 
            return 0
    return 1

def etalage(matrix):
    out = create_matrix(100, 100)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            k = 0
            up = matrix[max(0, min(100 - 1, i - 1))][j]
            if up != 0 : 
                k+=1
            down = matrix[max(0, min(100 - 1, i + 1))][j]
            if down != 0 : 
                k+=1
            left = matrix[i][max(0, min(100 - 1, j - 1))]
            if left != 0 : 
                k+=1
            right = matrix[i][max(0, min(100 - 1, j + 1))]
            if right != 0 : 
                k+=1
            mid = matrix[i][j]
            if mid != 0 : 
                k+=1
            if k == 0:
                k = 1
            out[i][j] = (up + down + left +right + mid)/k
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if out[i][j] > 1 :
                out[i][j] = 2 
            else : 
                out[i][j] = 1
            
    return out

class Wall():
    def __init__(self, a, b):
        #un mur est definit par ses deux extremités
        self.a = a
        self.b = b
        self.vector = vect(a,b)
        self.hitbox = hitbox(a, b)
        
    def display_wall(self):
        display_poly(self.hitbox)
        
    def is_in_wall(self, p):
        return is_in_poly(p, self.hitbox)
        
class Space():
    def __init__(self, nb_walls, h = 10, w = 10):
        self.h = h
        self. w = w
        self.nb_walls = nb_walls + 4
        self.walls = []
        for i in range(nb_walls):
            a = [r.uniform(0, self.w), r.uniform(0, self.h)]
            b = [r.uniform(0, self.w), r.uniform(0, self.h)]
            self.walls.append(Wall(a, b))
        self.walls.append(Wall([0, 0], [w, 0]))
        self.walls.append(Wall([w, 0], [w, h]))
        self.walls.append(Wall([w, h], [0, h]))
        self.walls.append(Wall([0, h], [0, 0]))
        #generer des murs aleatoirement ou un espace clos
        
    def display_space(self):
        for i in range(self.nb_walls):
            self.walls[i].display_wall()
        plt.xlim(-1, 11)
        plt.ylim(-1, 11)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
        
def matrixify(space, i = 100, j = 100):
    out = create_matrix(i, j)
    
    for k in range(i):
        for l in range(j):
            for wall in space.walls : 
                if is_in_poly([space.h*k/i, space.w*l/j], wall.hitbox):
                    out[k][l] = 1
                    
    return out

def line(matrix, a, b):
    ab = vect(a, b)
    
    for i in range(100):
        p = add(a, mult(ab, 1/100 * i))
        p[0], p[1] = int(p[0]), int(p[1])
        if matrix[p[0]][p[1]] == 1:
            return 0
    return 1
    
def is_even(x):
    if x % 2 == 0 : 
        return 1
    else : 
        return 0
   
def in_sight(out, matrix, p, mark):
    mi = len(matrix)
    mj = len(matrix[0])
    for i in range(mi):
        for j in range(mj):
            if line(matrix, p, [i,j]):
                if out[i][j] == 0 : 
                    out[i][j] = mark 
                elif is_even(out[i][j]) + is_even(mark) % 2 != 0 :
                    out[i][j] = 3
                else : 
                    pass
                
def far(out, matrix):
    mi = len(matrix)
    mj = len(matrix[0])
    for i in range(1, mi - 1):
        for j in range(1, mj - 1):
            if out[i + 1][j] != 0 and out[i - 1][j] != 0 and out[i][j + 1] != 0  and out[i][j - 1] != 0 :
                out[i][j] = 0.5
            else :
                pass
            
      
if __name__ == "__main__" : 
                    
    
    S = Space(5)
    M = matrixify(S, 50, 50)
    A = [45, 5] #depart
    B = [5, 45] #arrivée
    plt.imshow(M)
    plt.show()
    
    O = create_matrix(50, 50)
    
    in_sight(O, M, A, 1)
    in_sight(O, M, B, 2)
    far(O, M)
    
    
    
    plt.imshow(O)
    plt.show()
        
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CARTOGRAPHIE 2
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

def find_biggest(matrix):
    maxi = matrix[0][0]
    coord = [0,0]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > maxi : 
                maxi = matrix[i][j]
                coord = [i,j]
                
    return coord

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
        
class Agent():
    def __init__(self, position, space, i = 100, j = 100):
        self.i = i
        self.j = j
        self.intern_map = create_matrix(i, j)
        self.position = position
        self.speed = [0.1, 0.1]
        self.space = space
        self.is_in_wall = []
        for k in range(self.space.nb_walls):
            self.is_in_wall.append(False)
        
    def explore(self):
        
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        
        collision = False
        
        for j in range(len(self.space.walls)):
            wall = self.space.walls[j]
            if is_in_poly(self.position, wall.hitbox):
                collision = True
                if not self.is_in_wall[j]:
                    self.is_in_wall[j] = True
                    self.speed = rebond(self.speed, wall.vector)
                    
            else : 
                if self.is_in_wall[j]:
                    self.is_in_wall[j] = False
                    
        x = int(self.position[0] * self.i / self.space.w)
        y = int(self.position[1] * self.j / self.space.h)
                   
        if collision : 
            self.intern_map[y][x] = 2
        else : 
            self.intern_map[y][x] = 1
            
    def emptyest_square(self, nb = 10):
        matrix = self.intern_map
        scores = create_matrix(int(len(matrix)/nb), int(len(matrix[0])/nb))
        #découpage de la matrice en grille 10 par 10
        for i in range(nb):
            for j in range(nb):
                #pour chaque grille 10x10
                for k in range(int(len(matrix)/nb)):
                    for l in range(int(len(matrix[0])/nb)):
                        if matrix[int(k + i*len(matrix)/nb)][int(l + j*len(matrix[0])/nb)] == 0 : 
                            scores[i][j] += 1
        maxi = find_biggest(scores)
        #plt.imshow(scores)
        #plt.show()

        empty = maxi[0] * int(len(matrix)/nb), maxi[1] * int(len(matrix[0])/nb)   
        #print(normalize(vect(self.position,empty)))
        #print(empty)
        
        return normalize(vect(self.position,empty))
            
    def display_intern_map(self):
        plt.imshow(self.intern_map)
        plt.show()

S = Space(4, 10 ,10)
S.display_space()

A = Agent([5, 5], S)
for i in range(4000):
    A.explore()
    if i % 10 == 0:
        A.speed = add(A.speed, mult(A.emptyest_square(10), 0.1))
        if norm(A.speed) > 0.5 : 
            A.speed = mult(A.speed, 0.5)
            

A.intern_map = etalage(A.intern_map)
A.display_intern_map()   

B = Agent([5, 5], S)
for i in range(4000):
    B.explore()
    if norm(B.speed) > 0.5 : 
        B.speed = mult(B.speed, 0.5)

    

B.intern_map = etalage(B.intern_map)
B.display_intern_map()  


        
        
        

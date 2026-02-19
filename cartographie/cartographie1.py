#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le but de ce projet est de créer un agent dans un espace
cet agent est doté de capacité a se déplacer et il peut cartographier l'espace 
l'objectif se fait en deux phases : une phase d'exploration et de decouverte de l'espace 
et une phase de résolution : un endroit est pointé dans l'espace et l'agent doit y arriver le plus 
rapidement possible
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

def hitbox(a, b, w = 0.5):
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

    
def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]
       
def is_in_poly(a, poly):
    for i in range(len(poly)):
        d = dot(vect(poly[i - 1], a), vect(poly[i-1], poly[i]))
        if d < 0 : 
            return 0
    return 1
        
def proj(u, v):
    k = dot(u, v) / norm(v)**2
    return [v[0] * k, v[1] * k]

def rebond(u, v):
    #la formule 2 * proj(u sur v) - u est equivalent au rebond par rapport à la normale
    return add(mult(u, -1), mult(proj(u, v), 2))
        
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
        """
        l'agent est attiré par l'inconnu
        sa représentation interne est une matrice avec des cases 0, 1 et 2
        les cases 0 sont les cases pas encores explorées 
        les cases 1 sont les cases explorées 
        les cases 2 sont les cases identifiées comme des murs
        l'agent va chercher a atteindre les cases 0 et eviter les cases 2
        """
        """
        new_pos = add(self.speed, self.position)
        
        
        for i in range(self.space.nb_walls):
            wall = self.space.walls[i]
            
            if is_in_poly(new_pos, wall.hitbox):
                x = int(new_pos[0] * self.i / self.space.w)
                y = int(new_pos[1] * self.j / self.space.h)
                self.intern_map[y][x] = 2
                
                if not self.is_in_wall:
                    self.speed = rebond(self.speed, wall.vector)
                    self.is_in_wall = True
                break
            
            else :
                if i == self.space.nb_walls - 1:
                    self.is_in_wall = False
                    
                x = int(new_pos[0] * self.i / self.space.w) 
                
                y = int(new_pos[1] * self.j / self.space.h) 
                
                self.intern_map[y][x] = 1
                
        self.position = add(self.speed, self.position)
        """
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
        if x >= 99 or y >= 99:
            print("error")
            print(A.position)
            print(x, y)
            plt.imshow(A.intern_map, cmap = 'hot')
            plt.show()
            time.sleep(0.1)
            
                    
        if collision : 
            self.intern_map[y][x] = 2
        else : 
            self.intern_map[y][x] = 1
            
                
                    
                
               
        
        
    def aller(self, p):
        """
        avec un algorithme de recherche de chemin comme A* ou djikstra l'agent 
        pourra trouver un chemin pour atteindre le point pointé
        """
        
def vectorfield(matrix, agent):
    vector = [0, 0]
    K = [-2, 0, 5]
    C = [1, 1, 1]
    
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            
            r = vect([i,j], agent)
            d = norm(r) 
            
            k = None
            for l in range(len(K)):
                if matrix[i][j] == l:
                    C[l] += 1
                    k = K[l] / C[l]
                
                    
            e = 0.1
            
            f = mult(r, k/1000)
            
            vector[0] += f[0]
            vector[1] += f[1]
 
    return vector
    
"""
a = (0, 0)
b = (1, 1)
c = (0.5, 0.5)
poly = hitbox(a, b, 0.5)
plt.scatter(c[0], c[1])
display_poly(poly)
print(is_in_poly(c, poly))
"""

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

def mirror(matrix):
    out = [[0 for i in range(len(matrix[0]))] for i in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            out[i][j] = matrix[len(matrix) - 1 - i][j]
    return out
            

                


S = Space(5)
S.display_space()
plt.xlim(-1, 11)
plt.ylim(-1, 11)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
plt.show()


A = Agent([5,5], S)
for i in range(1000):
    A.explore()

    f = vectorfield(A.intern_map, A.position)
    A.speed = add(A.speed, mult(f, 0.1))
    if norm(A.speed) > 0.5:
        A.speed = mult(A.speed, 0.5)

    plt.imshow(A.intern_map, cmap = 'hot')
    plt.show()
    
A.intern_map = mirror(A.intern_map)
    
plt.imshow(A.intern_map, cmap = 'hot')
plt.show()
    
out = etalage(A.intern_map)
out = etalage(out)



plt.imshow(out, cmap = 'hot')
plt.show()
    #time.sleep(0.5)

        
        
        



# -*- coding: utf-8 -*-
"""
chemins Monte Carlo
"""

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



def line_test(matrix, A, B):
    AB = vect(A, B)
    depart = A
    position = A
    
    k = int(AB[0]/abs(AB[0])) if AB[0] != 0 else 0
    l = int(AB[1]/abs(AB[1])) if AB[1] != 0 else 0

    
    while True : 
        global ops 
        ops += 1
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
    def __init__(self, size, matrix, A, B):
        self.size = size + 2
        self.mi = len(matrix)
        self.mj = len(matrix[0])
        self.nodes = [Node(A), Node(B)]
        for i in range(self.size):
            x = r.randint(0, self.mi - 1)
            y = r.randint(0, self.mj - 1)
            self.nodes.append(Node([x,y]))
            
    def watching(self, matrix):
        #watching créé un graph de visibilité
        self.nodes[0].degreA = 0
        self.nodes[0].distA = 0
        self.nodes[1].degreB = 0
        self.nodes[1].distB = 0
        for i in range(self.size):
            #on regarde seulement les binomes uniques
            for j in range(i + 1, self.size):
                global ops 
                ops += 1
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
        changed = True
        while changed : 
            changed = False
            for i in range(self.size):
                for j in range(len(self.nodes[i].links)):
                    global ops 
                    ops += 1
                    node = self.nodes[i].links[j]
                    distanceA = node.distA + self.nodes[i].dists[j]
                    if distanceA < self.nodes[i].distA : 
                        self.nodes[i].distA = distanceA
                        changed = True
                    if node.distA > self.nodes[i].distA + self.nodes[i].dists[j]: 
                        node.distA = self.nodes[i].distA + self.nodes[i].dists[j]
                        changed = True
                    distanceB = node.distB + self.nodes[i].dists[j]
                    if distanceB < self.nodes[i].distB : 
                        self.nodes[i].distB = distanceB
                        changed = True    
                    if node.distB  > self.nodes[i].distB + self.nodes[i].dists[j] : 
                        node.distB = self.nodes[i].distB + self.nodes[i].dists[j]
                        changed = True      
                self.nodes[i].total = self.nodes[i].distA + self.nodes[i].distB
                
    def find(self):
        best_node = self.nodes[0]
        # on pourrait ici reconstruire un chemin vers B
        # en suivant toujours le voisin avec distB minimal
        path = [best_node.position]
        current = best_node
        while current.degreB != 0:
            global ops 
            ops += 1
            # choisir le lien avec distB minimal
            next_node = min(current.links, key=lambda n: n.distB)
            if next_node.position in path:
                
                break  # boucle
            path.append(next_node.position)
            current = next_node   
        return path
            
def path_finding(MCsize, matrix, A, B):
    S = Simulation(MCsize, matrix, A, B)       
    S.watching(matrix)
    S.find_path()
    return S.find()





                        
            
        
import random as r
from algebra import dist
from raytracing import line_test
import matplotlib.pyplot as plt

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
            
        self.path = None
            
    def watching(self, matrix):
        #watching créé un graph de visibilité
        self.nodes[0].degreA = 0
        self.nodes[0].distA = 0
        self.nodes[1].degreB = 0
        self.nodes[1].distB = 0
        for i in range(self.size):
            #on regarde seulement les binomes uniques
            for j in range(i + 1, self.size):

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
            # choisir le lien avec distB minimal
            next_node = min(current.links, key=lambda n: n.distB)
            if next_node.position in path:
                
                break  # boucle
            path.append(next_node.position)
            current = next_node   
        self.path = path
    
    def display_graph(self):
        for i in range(self.size):
            for j in range(len(self.nodes[i].links)):
                x1 = self.nodes[i].position[1]
                x2 = self.nodes[i].links[j].position[1]
                y1 = -self.nodes[i].position[0]
                y2 = -self.nodes[i].links[j].position[0]
                x = [x1, x2]
                y = [y1, y2]
                plt.plot(x, y, linewidth = 0.1)
        plt.xlim(0, 50)
        plt.ylim(-50, 0)
        plt.gca().set_aspect('equal', adjustable='box')
        
        for i in range(len(self.path) - 1):
            x1 = self.path[i][1]
            x2 = self.path[i + 1][1]
            y1 = -self.path[i][0]
            y2 = -self.path[i + 1][0]
            x = [x1, x2]
            y = [y1, y2]
            plt.plot(x, y, color = 'black', linewidth = 2)
        plt.xlim(0, 50)
        plt.ylim(-50, 0)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
            
def path_finding(MCsize, matrix, A, B):
    S = Simulation(MCsize, matrix, A, B)       
    S.watching(matrix)
    S.find_path()
    S.find()
    S.display_graph()
    return S.path





                        
            
        
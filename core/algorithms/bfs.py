#!/usr/bin/env python
from collections import deque
import pygraphviz as pgv
class Bfs(object):
    def __init__(self,G,V):
        self.G = G
        self.V = V
        self.descendants = []
    def _traverse(self):
        nonemptyQueue = deque('')
        v = self.G.get_node(self.V)
        nonemptyQueue.append(v)
        while len(nonemptyQueue) is not 0:
            temp = nonemptyQueue.popleft()
            for neighbor in self.G.successors(temp):
                if not neighbor in self.descendants:
                    self.descendants.append(neighbor)
                    nonemptyQueue.append(neighbor)
        
    def getDescendants(self):
        self._traverse()
        return self.descendants
class Descendants(object):
    def __init__(self,G1,G2,V):
        self.G1 = G1
        self.G2 = G2
        self.V = V
    def getDescendats(self):
        bfs = Bfs(self.G1,self.V)
        descendants1 = bfs.getDescendants()
        bfs2 = Bfs(self.G2,self.V)
        descendants2 = bfs2.getDescendants()
        descendants1set = set(descendants1)
        descendants2set = set(descendants2)
        descendantsset = descendants2set - descendants1set
        return list(descendantsset)
        
class NewDescendats(Descendants):
    def __init__(self,G1,G2,V):
        Descendants.__init__(self,G1,G2,V)
    def getDescendats(self):
        descendants = []
        nonemptyQueue = deque('')
        v = self.G1.get_node(self.V)
        successors = self.G1.successors(v)
        nonemptyQueue.append(v)
        while nonemptyQueue:
            temp = nonemptyQueue.popleft()
            for successor in self.G2.successors(temp):
                if not successor in successors:
                    descendants.append(successor)
                    nonemptyQueue.append(successor)
        return descendants
    
if __name__ == '__main__':
    G = pgv.AGraph()
    G2 = pgv.AGraph()
    elist=[('A','B'),('A','C'),('B','D')]
    elist2=[('A','B'),('A','C'),('A','M'),('B','D'),('D','E'),('E','F'),('F','H')]
    G.add_edges_from(elist)
    G2.add_edges_from(elist2)
    g1nodes = G.nodes()
    S = {}
    for node in g1nodes:
        print node
        newDescendants = NewDescendats(G,G2,node)
        descendantsList = newDescendants.getDescendats()
        # descendantsList = newDescendants.getDescendats()
        ng1 = G.neighbors(node)
        print 'lenght of neighbors {}'.format(len(ng1))
        print 'lenght of new descendants {}'.format(len(descendantsList))
        S[node] = len(ng1) + len(descendantsList)

    # print descendantsList

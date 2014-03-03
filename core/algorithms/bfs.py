#!/usr/bin/env python
from collections import deque
import pygraphviz as pgv
import logging
log = logging.getLogger(__name__)
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
        v1 = self.G1.get_node(self.V)
        v2 = self.G2.get_node(self.V)
        bfs = Bfs(self.G1,v1)
        descendants1 = bfs.getDescendants()
        bfs2 = Bfs(self.G2,v2)
        descendants2 = bfs2.getDescendants()
        descendants1set = set(descendants1)
        descendants2set = set(descendants2)
        descendantsset = descendants2set - descendants1set
        return list(descendantsset)
        
class NewDescendats(Descendants):
    def __init__(self,G1,G2,V):
        log.info('initializing NewDescendants')
        Descendants.__init__(self,G1,G2,V)
    def getDescendats(self):
        log.info('getting Descendants if %s',str(self.V))
        descendants = []
        nonemptyQueue = deque('')
        successors = self.G1.successors(self.V)
        for i in successors:
            log.info('successor %s of %s',str(i),str(self.V))
        log.info('size of self.V sucessors %s in G1',len(successors))
        nonemptyQueue.append(self.V)
        while nonemptyQueue:
            temp = nonemptyQueue.popleft()
            log.info('temp is %s',str(temp))
            for successor in self.G2.successors(temp):
                log.info('succesors is %s',str(successor))
                if not successor in successors:
                    descendants.append(successor)
                    nonemptyQueue.append(successor)
        log.info('size of descendants list is %s',len(descendants))
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

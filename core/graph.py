import logging
import pygraphviz as pgv

log = logging.getLogger(__name__)

class Graph(pgv.AGraph):
    def get_root(self):
        for n,d in self.in_degree_iter():
            if d is 0:
                root = n
        return root    
    def get_number_of_children(self,node):
        return len(self.successors(node))


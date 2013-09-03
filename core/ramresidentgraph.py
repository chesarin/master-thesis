import logging
import sys
import pydot
from interfaces.iphylogeny import IPhylogeny
from ramresidentmc import RamResidentMC

log = logging.getLogger(__name__)

class RAMResidentGraph(IPhylogeny):
    
    def __init__(self):
        self.corpus = RamResidentMC()
        self.malware_edges = []
        self.malware_nodes = []
        self.corpus_hash = {}
        self.graph = pydot.Dot(graph_type='digraph')

    def set_corpus(self,incorpus):
        if self.corpus.get_size() == 0:
            self.corpus = incorpus
        else:
            sys.exit("corpus already set")
    
    def add_node(self,malware):
        if (self.corpus.is_present(malware)):
            node = pydot.Node(self.get_location(malware))
            self.graph.add_node(node)
            self.malware_nodes.append(node)
        else:
            sys.exit("malware not in corpus")

    def add_edge(self,malware1,malware2,distance):
        log.info('parameters:%s %s %s',malware1,malware2,str(distance))
        if (self.corpus.is_present(malware1) &
            self.corpus.is_present(malware2)):
            edge = pydot.Edge(self.get_location(malware1),
                              self.get_location(malware2),
                              label=str(distance))
            self.graph.add_edge(edge)
            self.malware_edges.append(edge)
        else:
            sys.exit("malware1 or malware2 not in corpus")

    def write_graphiz_file(self,filename):
        self.graph.write_png(filename)
        
    def create_corpus_hash(self):
        for location in range(self.corpus.get_size()):
            self.corpus_hash[self.corpus.getNthCronological(location)] = location
    
    def get_corpus(self):
        return self.corpus

    def get_location(self,malware):
        return self.corpus_hash[malware]

    def is_edge(self,malwareu,malwarev):
        """Nothing for now"""
        return

    def print_edges(self):
        self.create_corpus_hash()
        for i in self.malware_edges:
            log.info( '%s %s %s', self.get_location(i[0]),
                    self.get_location(i[1]), i[2])






import logging
import sys
from interfaces.iphylogeny import IPhylogeny
from ramresidentmc import RamResidentMC
from graph import Graph

log = logging.getLogger(__name__)

class RAMResidentGraph(IPhylogeny):
    
    def __init__(self):
        self.corpus = RamResidentMC()
        self.corpus_hash = {}
        self.graph = Graph()

    def set_corpus(self,incorpus):
        """Set the corpus from the incorpus object. Once that is
        done then sort the corpus from earliest to latest sample than
        create a hash for lookup locations. 
        I need better check for this section"""
        if self.corpus.get_size() == 0:
            self.corpus = incorpus
            self.corpus.mc_sort()
            self.create_corpus_hash()
        else:
            sys.exit("corpus already set")
            
    def create_corpus_hash(self):
        """Set a lookup table for the malware corpus.
        We want to use the malware sample as the key
        and the chronological order as the value."""
        for location in range(self.corpus.get_size()):
            self.corpus_hash[self.corpus.getNthCronological(location)] = location
            
    def add_node(self,malware):
        if (self.corpus.is_present(malware)):
            self.graph.add_node(malware,comment=str(malware.get_date()))
        else:
            sys.exit("malware not in corpus")

    def add_edge(self,malware1,malware2,distance):
        log.info('parameters:%s %s %s',malware1,malware2,str(distance))
        if (self.corpus.is_present(malware1) &
            self.corpus.is_present(malware2)):
            log.info('adding edge as follows')
            log.info('malware 1 %s with date %s',malware1,str(malware1.get_date()))
            log.info('malware 2 %s with date %s',malware2,str(malware2.get_date()))
            self.graph.add_node(malware1,comment=str(malware1.get_date()))
            self.graph.add_node(malware1,comment=str(malware2.get_date()))
            self.graph.add_edge(malware1,malware2,distance)
        else:
            sys.exit("malware1 or malware2 not in corpus")
            
    def get_corpus(self):
        return self.corpus
        
    def get_location(self,malware):
        return self.corpus_hash[malware]

    def get_graph(self):
        return self.graph
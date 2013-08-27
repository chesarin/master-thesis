import logging
import sys
import pydot
from interfaces.iphylogeny import IPhylogeny
from ramresidentmc import RamResidentMC

log = logging.getLogger(__name__)

class RAMResidentGraph(IPhylogeny):
	
	def __init__(self):
		self.corpus = RamResidentMC()
		self.malware_pairs = []
		self.corpus_hash = {}

	def set_corpus(self,incorpus):
		if self.corpus.get_size() == 0:
			self.corpus = incorpus
		else:
			sys.exit("corpus already set")
	
	def add_edge(self,malware1,malware2,distance):
		if (self.corpus.is_present(malware1) &
			self.corpus.is_present(malware2)):
			edge = (malware1,malware2,distance)
			self.malware_pairs.append(edge)
		else:
			sys.exit("malware1 or malware2 not in corpus")

	def write_graphiz_file(self,filename):
		if len(self.corpus_hash) == 0:
			self.create_corpus_hash()
		graph = pydot.Dot(graph_type='digraph')
		for i in self.malware_pairs:
			node1 = self.get_location(i[0])
			node2 = self.get_location(i[1])
			edge = pydot.Edge(node1,node2,label=str(i[2]))
			graph.add_edge(edge)
		graph.write_png(filename)
		
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
		for i in self.malware_pairs:
			log.info( '%s %s %s', self.get_location(i[0]),
					self.get_location(i[1]), i[2])






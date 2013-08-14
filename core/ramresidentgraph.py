import logging
import sys
from interfaces.iphylogeny import IPhylogeny
from ramresidentmc import RamResidentMC

log = logging.getLogger(__name__)

class RAMResidentGraph(IPhylogeny):
	
	def __init__(self):
		self.corpus = RamResidentMC()
		self.malware_pairs = []

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

	def write_graphiz_file(self,path):
		"""Nothing for now"""
		return

	def get_corpus(self):
		return self.corpus

	def is_edge(self,malwareu,malwarev):
		"""Nothing for now"""
		return

	def print_edges(self):
		for i in self.malware_pairs:
			log.info( '%s %s %s', i[0], i[1], i[2])



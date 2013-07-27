#!/usr/bin/env python
from interfaces.imalwarecorpus import IMalwareCorpus

class RamResidentMC(IMalwareCorpus):

	def __init__(self):
		self.mcorpus = []
	
	def add(self,malware):
		self.mcorpus.append(malware)

	def get_size(self):
		return len(self.mcorpus)

	def is_present(self,malware):
		return 'test'
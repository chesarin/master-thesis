#!/usr/bin/env python
import os
from malwarecorpusfactory import MalwareCorpusFactory
from ramresidentmc import RamResidentMC
from apkmalware import ApkMalware

class APKDirectoryFactory(MalwareCorpusFactory):
	def __init__(self):
		self.ramcorpus = RamResidentMC

	def create(self,directory):
		listing = os.listdir(directory)
		for file in listing:
			temp = directory+'/'+file
			self.process_apk_file(temp)

	def process_apk_file(self,file):
		try:
			apk = ApkMalware(file)
			self.ramcorpus.add(apk)
		except:
			print "Non-APk File"
		
		

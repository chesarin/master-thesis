#!/usr/bin/env python
import os
from malwarecorpusfactory import MalwareCorpusFactory
from ramresidentmc import RamResidentMC
from apkmalware import ApkMalware

class APKDirectoryFactory(MalwareCorpusFactory):
	
	def create(self,directory):
		self.ramcorpus = RamResidentMC
		listing = os.listdir(directory)
		for file in listing:
			temp = directory+'/'+apkfile
			self.process_apk_file(temp)

	def process_apk_file(self,file):
		try:
			apk = ApkMalware(file)
			self.ramcorpus.add(apk)
		except:
			print "Non-APk File"
		
		

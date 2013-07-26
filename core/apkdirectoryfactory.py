#!/usr/bin/env python
import os
import logging
from interfaces.imalwarecorpusfactory import IMalwareCorpusFactory
from ramresidentmc import RamResidentMC
from apkmalware import ApkMalware

class APKDirectoryFactory(IMalwareCorpusFactory):

	def __init__(self):
		self.ramcorpus = RamResidentMC()
		self.validapk = 0
		self.nonvalidapk = 0

	def create(self,directory):
		listing = os.listdir(directory)
		for file in listing:
			temp = directory+"/"+file
			logging.warning("File name "+temp)
			self.process_apk_file(temp)

	def process_apk_file(self,file):
		logging.warning("inside process apk files")
		try:
			logging.warning("Creating APK object")
			apk = ApkMalware(file)
			logging.warning("Adding APK object to ramcorpus")
			self.ramcorpus.add(apk)
			logging.warning("incrementing counter for validapk")
			self.validapk += 1
		except:
			logging.warning("Exception why")
			self.nonvalidapk += 1
		
		

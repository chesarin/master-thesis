#!/usr/bin/env python
#from core.apkdirectoryfactory import APKDirectoryFactory
from core.testmalwaredirectoryfactory import TestMalwareDirectoryFactory
from core.losslessfingerprintfactory import LosslessFingerPrintFactory
from core.zipmetric import ZipMetric
from core.treefactory import TreeFactory

def main():
	print 'Contorller Start'
	directory1 = '/Users/punisher/Documents/master-thesis/data'
	dfactory = TestMalwareDirectoryFactory()
	dfactory.create(directory1)
	mc = dfactory.get_corpus()
	fpf = LosslessFingerPrintFactory()
	dis = ZipMetric()
	treefactory = TreeFactory()
	result = treefactory.create(mc,fpf,dis)
	print 'Controller Ends'

if __name__ == "__main__":
	main()

#!/usr/bin/env python
#from core.apkdirectoryfactory import APKDirectoryFactory
import logging
from core.testmalwaredirectoryfactory import TestMalwareDirectoryFactory
from core.losslessfingerprintfactory import LosslessFingerPrintFactory
from core.zipmetric import ZipMetric
from core.treefactory import TreeFactory


def main():
	logging.basicConfig(filename='application.log',
						filemode='w',
						level=logging.INFO,
						format='%(asctime)s %(name)s %(message)s', 
						datefmt='%m/%d/%Y %I:%M:%S %p')
	log = logging.getLogger(__name__) 
	log.info('Controller Start')
	directory1 = '/Users/punisher/Documents/master-thesis/data'
	dfactory = TestMalwareDirectoryFactory()
	dfactory.create(directory1)
	mc = dfactory.get_corpus()
	fpf = LosslessFingerPrintFactory()
	dis = ZipMetric()
	treefactory = TreeFactory()
	result = treefactory.create(mc,fpf,dis)
	log.info('Controller Ends')

if __name__ == "__main__":
	main()

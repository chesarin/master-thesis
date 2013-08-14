#!/usr/bin/env python
#from core.apkdirectoryfactory import APKDirectoryFactory
import logging
import argparse
from core.testmalwaredirectoryfactory import TestMalwareDirectoryFactory
from core.losslessfingerprintfactory import LosslessFingerPrintFactory
from core.zipmetric import ZipMetric
from core.treefactory import TreeFactory


def main():
	log = logging.getLogger(__name__) 
	parser = argparse.ArgumentParser()
	parser.add_argument("-q","--quiet",
						help="Display only error messages",
						action="store_true",required=False)
	parser.add_argument("-d","--debug",
						help="Display debug messages",
						action="store_true",required=False)
	parser.add_argument("-dir","--directory",
						help="Directory to read malware from",
						default="/Users/punisher/Documents/master-thesis/data",
						required=False)
	args = parser.parse_args()
	dic_args = vars(args)

#	if args.quiet:
#		log.setLevel(logging.WARN)
#	elif args.debug:
#		log.setLevel(logging.DEBUG)

	logging.basicConfig(filename='application.log',
						filemode='w',
						level=logging.DEBUG,
						format='%(asctime)s %(name)s %(funcName)s %(message)s', 
						datefmt='%m/%d/%Y %I:%M:%S %p')


	log.info('Controller Start')
	dfactory = TestMalwareDirectoryFactory()
	dfactory.create(dic_args['directory'])
	mc = dfactory.get_corpus()
	fpf = LosslessFingerPrintFactory()
	dis = ZipMetric()
	treefactory = TreeFactory()
	result = treefactory.create(mc,fpf,dis)
	log.info('Controller Ends')

if __name__ == "__main__":
	main()

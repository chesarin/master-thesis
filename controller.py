#!/usr/bin/env python
import logging
import argparse
from core.testmalwaredirectoryfactory import TestMalwareDirectoryFactory
from core.losslessfingerprintfactory import LosslessFingerPrintFactory
from core.apkdirectoryfactory import APKDirectoryFactory
from core.androidmanifestfingerprintfactory import AndroidManifestFingerPrintFactory
#from core.zipmetric import ZipMetric
from core.bytesmetric import BytesMetric
from core.ncdmetric import NCDMetric
from core.ratcliffmetric import RatcliffMetric
from core.treefactory import TreeFactory
from core.dagfactory import DAGFactory
# from core.njtreefactory import NjTreeFactory
from core.perfectpredictionfactory import PerfectPredictionFactory
from core.graphutils import GraphJson
from core.childcountpredfactory import ChildCountPredFactory 

log = logging.getLogger(__name__) 

def init_logging(args):
    if args.quiet:
        logging.basicConfig(filename='application.log',
                            filemode='w',
                            level=logging.WARN,
                            format='%(asctime)s %(name)s %(funcName)s %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    elif args.debug:
        logging.basicConfig(filename='application.log',
                            filemode='w',
                            level=logging.DEBUG,
                            format='%(asctime)s %(name)s %(funcName)s %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p')

def init_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q","--quiet",
                        help="Display only error messages",
                        action="store_true",required=False)
    parser.add_argument("-d","--debug",
                        help="Display debug messages",
                        action="store_true",required=False)
    parser.add_argument("-dir1","--directory1",
                        help="Directory1 to read malware from",
                        default="test-data/past-data",
                        required=False)
    parser.add_argument("-dir2","--directory2",
                        help="Directory2 to read malware from",
                        default="test-data/present-data",
                        required=False)
    parser.add_argument("-result1","--resultfilename1",
                        help="Output file for Phylogeny1 Graph created",
                        default="output/graph1.png",
                        required=False)
    parser.add_argument("-result2","--resultfilename2",
                        help="Output file for Phylogeny2 Graph created",
                        default="output/graph2.png",
                        required=False)

    return parser

def create_phylogeny(directory,outputfilename):
    # dfactory = TestMalwareDirectoryFactory()
    dfactory = APKDirectoryFactory()
    dfactory.create(directory)
    mc = dfactory.get_corpus()
    fpf = AndroidManifestFingerPrintFactory()
    # fpf = LosslessFingerPrintFactory()
    # dis = ZipMetric()
    # dis = BytesMetric()
    dis = RatcliffMetric()
    # dis = NCDMetric()
    treefactory = DAGFactory(0.6)
    # treefactory = TreeFactory()
    # treefactory = NjTreeFactory()
    phylogeny1 = treefactory.create(mc,fpf,dis)
    json = GraphJson(phylogeny1)
    # json.create_json_for_graph(outputfilename)
    json.create_json_file(outputfilename)
    json.create_edges_file('output/test.txt')
    return phylogeny1

def create_prediction(phylogeny1,phylogeny2):
    prefactory = ChildCountPredFactory()
    prediction = prefactory.makePrediction(phylogeny1,phylogeny2)
    
def main():
    """Initiate arguments, logs and dictionary to be used to extract parameters"""
    parser = init_arguments()
    args = parser.parse_args()
    dic_args = vars(args)
    init_logging(args)
    """Actual Works Start Here"""
    log.info('Starts')
    phy1 = create_phylogeny(dic_args['directory1'],
                            dic_args['resultfilename1'])
    
    phy2 = create_phylogeny(dic_args['directory2'],
                            dic_args['resultfilename2'])
    create_prediction(phy1,phy2)
    # perfectpre = PerfectPredictionFactory()
    # perfectpre.create(phy1,phy2)
    log.info('Ends')

if __name__ == "__main__":
    main()

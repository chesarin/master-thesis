#!/usr/bin/env python
import logging
import argparse
from core.testmalwaredirectoryfactory import TestMalwareDirectoryFactory
from core.losslessfingerprintfactory import LosslessFingerPrintFactory
from core.apkdirectoryfactory import APKDirectoryFactory
from core.androidmanifestfingerprintfactory import AndroidManifestFingerPrintFactory
from core.zipmetric import ZipMetric
from core.bytesmetric import BytesMetric
from core.ncdmetric import NCDMetric
from core.ratcliffmetric import RatcliffMetric
from core.treefactory import TreeFactory
from core.dagfactory import DAGFactory
# from core.sdhashmetric import SdhashMetric
# from core.njtreefactory import NjTreeFactory
from core.perfectpredictionfactory import PerfectPredictionFactory
from core.graphutils import GraphJson
from core.childcountfactoryperfectprediction import ChildCountFactoryPerfectPrediction 
from core.treemodel import TreeModel
from core.childcountscore import ChildCountScore
from core.avedivergence import AveDivergence
from core.maxdivergence import MaxDivergence
from core.phylogenyfactory import PhylogenyFactory
from core.disdb import DisDB
from tools.predictionsdb import PredictionsDB
from tools.rgraph import Rgraph


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

def create_phylogeny(directory):
    dfactory = APKDirectoryFactory()
    fpf = AndroidManifestFingerPrintFactory()
    dis = RatcliffMetric()
    treefactory = TreeFactory()
    phylogenyfactory = PhylogenyFactory(directory,dfactory,fpf,dis,treefactory)
    return phylogenyfactory.get_phylogeny()
    
def create_dis_db(directory,outdir):
    log.info('starting distance db')
    dfactory = APKDirectoryFactory()
    fpf = AndroidManifestFingerPrintFactory()
    dis = RatcliffMetric()
    db = DisDB(directory,dis,fpf,dfactory)
    db.create_file(outdir)
    return db
    
def create_perfect_prediction(phylogeny1,phylogeny2):
    log.info('creating perfect prediction')
    # scorer = ChildCountScore()
    # predictor = TreeModel()
    # predictor.setScorer(scorer)
    # prediction1 = predictor.makePre(phylogeny1)
    prefactory = ChildCountFactoryPerfectPrediction()
    pprediction = prefactory.makePrediction(phylogeny1,phylogeny2)
    log.info('done with the perfect prediction')
    return pprediction
    # divergence = AveDivergence()
    # divergence.calcDiv(prediction1,actualprediction)

def create_my_prediction(phylogeny1):
    log.info('creating myprediction')
    scorer = ChildCountScore()
    predictor = TreeModel()
    predictor.setScorer(scorer)
    myprediction = predictor.makePre(phylogeny1)
    log.info('done with myprediction')
    return myprediction
    # prefactory = ChildCountPredFactory()
    # actualprediction = prefactory.makePrediction(phylogeny1,phylogeny2)
    # divergence = AveDivergence()
    # divergence.calcDiv(prediction1,actualprediction)
    
def execute(dir1,dir2,outputdir='/tmp/output'):
    log.info('starting execute function')
    disdb = create_dis_db(dir1,outputdir)
    phy1 = create_phylogeny(dir1)
    phy2 = create_phylogeny(dir2)
    myprediction = create_my_prediction(phy1)
    pprediction = create_perfect_prediction(phy1,phy2)
    predictiondb = PredictionsDB(myprediction,pprediction)
    predictiondb.create_file(outputdir)
    rgraph = Rgraph(predictiondb,disdb,outputdir)
    log.info('ending execute function')
    
def main():
    """Initiate arguments, logs and dictionary to be used to extract parameters"""
    parser = init_arguments()
    args = parser.parse_args()
    init_logging(args)
    """Actual Works Start Here"""
    log.info('Starts')
    execute(args.directory1,args.directory2)
    # disdb = create_dis_db(args.directory1)
    # phy1 = create_phylogeny(args.directory1,
    #                         args.resultfilename1)
    
    # phy2 = create_phylogeny(args.directory2,
    #                         args.resultfilename2)
    # myprediction=create_my_prediction(phy1)
    # pprediction=create_perfect_prediction(phy1,phy2)
    # predictiondb = PredictionsDB(myprediction,pprediction)
    # predictiondb.create_file()
    # rgraph = Rgraph(predictiondb,disdb)
    log.info('Ends')

if __name__ == "__main__":
    main()

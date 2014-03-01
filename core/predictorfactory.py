#!/usr/bin/env python
import logging
from disdb import DisDB
from treefactory import TreeFactory
from treemodel import TreeModel
from core.phylogeny.phylogenyfactory import PhylogenyFactory
from childcountscore import ChildCountScore
from core.predictions.perfectpredictions.neighborcountfactorypprediction import NeighborCountFactoryPPrediction
from statistics.predictionstats import PredictionStats
from core.plots.xyplot import XyPlot
from predictionsdb import PredictionsDB
log = logging.getLogger(__name__)

class PredictorFactory(object):
    def __init__(self,dir1,dir2,outputdir='/tmp/output'):
        log.info('initializing PredictorFactory')
        self.dir1 = dir1
        self.dir2 = dir2
        self.outputdir = outputdir
        self.treefactory = TreeFactory()
    def set_factories(self,dfactory,fpf,dis):
        log.info('Setting factorites')
        self.dfactory = dfactory
        self.fpf = fpf
        self.dis = dis
    def execute(self):
        log.info('executing PredictorFactory')
        self.create_dis_db()
        self.create_phylogenies()
        self.create_my_prediction()
        self.create_perfect_prediction()
        self.create_predictiondb()
        # self.calc_statistics()
    def create_dis_db(self):
        self.db = DisDB(self.dir1,self.dis,self.fpf,self.dfactory)
        self.db.create_file(self.outputdir)
    def create_phylogenies(self):
        phylogenyfactory1 = PhylogenyFactory(self.dir1,self.dfactory,self.fpf,self.dis,self.treefactory)
        phylogenyfactory2 = PhylogenyFactory(self.dir2,self.dfactory,self.fpf,self.dis,self.treefactory)
        self.phy1 = phylogenyfactory1.get_phylogeny()
        self.phy2 = phylogenyfactory2.get_phylogeny()
    def create_my_prediction(self):
        scorer = ChildCountScore()
        predictor = TreeModel()
        predictor.setScorer(scorer)
        self.myprediction = predictor.makePre(self.phy1)
    def create_perfect_prediction(self):
        prefactory = NeighborCountFactoryPPrediction()
        self.pprediction = prefactory.makePrediction(self.phy1,self.phy2)
    def create_predictiondb(self):
        self.predictiondb = PredictionsDB(self.myprediction,self.pprediction)
        self.predictiondb.create_file(self.outputdir)
    def get_statistics(self):
        pstats = PredictionStats(self.predictiondb)
        return pstats.get_stats()
    def plot_predictions(self):
        plot = XyPlot(self.predictiondb)
        plot.pdfPlot(self.outputdir)

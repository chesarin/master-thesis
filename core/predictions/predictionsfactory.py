#!/usr/bin/env python
"""predictionsfactory module"""
import logging
# from disdb import DisDB
from core.phylogeny.trees.treemodel import TreeModel
from core.predictions.treemodel import TreeModel as PredictionsTreeModel
from core.phylogeny.phylogenyfactory import PhylogenyFactory
from core.predictions.prediction.childcountscore import ChildCountScore
from core.predictions.perfectpredictions.neighborcountfactorypprediction import NeighborCountFactoryPPrediction
from core.predictions.perfectpredictions.newdescendantscountfactorypprediction import NewDescendatsCountFactoryPPrediction
from core.predictions.predictionvisualizer import PredictionVisualizer
from core.statistics.predictionstats import PredictionStats
from core.plots.xyplot import XyPlot
from predictionsdb import PredictionsDB
log = logging.getLogger(__name__)

class PredictionsFactory(object):
    """PredictionsFactory class"""
    def __init__(self, dir1, dir2, outputdir='/tmp/output'):
        """Constructor uses dir1, dir2 and outputdir to create predctions"""
        log.info('initializing PredictorFactory')
        self.dir1 = dir1
        self.dir2 = dir2
        self.outputdir = outputdir
        self.treefactory = TreeModel()
    def set_factories(self, dfactory, fpf, dis):
        """we need a few factories like dfactory, fingerprintfactory
        and a distance metric"""
        log.info('Setting factorites')
        self.dfactory = dfactory
        self.fpf = fpf
        self.dis = dis
    def execute(self):
        """the execute funtions creates the phylogenies
        mypredictions, the perfect predictiona and the predictiondb"""
        log.info('executing PredictorFactory')
        # self.create_dis_db()
        self.create_phylogenies()
        self.create_my_prediction()
        self.create_perfect_prediction()
        self.create_predictiondb()
        self.prediction_visualizer()
        # self.calc_statistics()
    # def create_dis_db(self):
    #     self.db = DisDB(self.dir1,self.dis,self.fpf,self.dfactory)
    #     self.db.create_file(self.outputdir)
    def create_phylogenies(self):
        """create phylogenies create each phylogeny for each directory"""
        phylogenyfactory1 = PhylogenyFactory(self.dir1, self.dfactory,
                                             self.fpf, self.dis,
                                             self.treefactory)
        phylogenyfactory2 = PhylogenyFactory(self.dir2, self.dfactory,
                                             self.fpf, self.dis,
                                             self.treefactory)
        self.phy1 = phylogenyfactory1.get_phylogeny()
        self.phy2 = phylogenyfactory2.get_phylogeny()
        self.phy1.write_graphviz(self.outputdir, 'phylogeny1')
        self.phy2.write_graphviz(self.outputdir, 'phylogeny2')
    def create_my_prediction(self):
        """create_my_prediction uses phylogeny1 to create the prediction"""
        scorer = ChildCountScore()
        predictor = PredictionsTreeModel()
        predictor.setScorer(scorer)
        self.myprediction = predictor.makePre(self.phy1)
    def create_perfect_prediction(self):
        """create perfect prediction utilizes phy1 and phy2 to
        create perfect predictions"""
        # prefactory = NeighborCountFactoryPPrediction()
        prefactory = NewDescendatsCountFactoryPPrediction()
        self.pprediction = prefactory.makePrediction(self.phy1,
                                                     self.phy2)
    def create_predictiondb(self):
        """we store the predictions in a predictions db object"""
        self.predictiondb = PredictionsDB(self.myprediction,
                                          self.pprediction)
        self.predictiondb.create_predictions()
        self.predictiondb.create_file(self.outputdir)
    def get_statistics(self):
        """we use the predictiondb to get statistics"""
        pstats = PredictionStats(self.predictiondb)
        return pstats.get_stats()
    def plot_predictions(self):
        """we plot the predictions using an xyplot"""
        x = self.predictiondb.get_perfect_prediction()
        y = self.predictiondb.get_my_prediction()
        plot = XyPlot(x,y)
        plot.plot_pdf(self.outputdir)
    def prediction_visualizer(self):
        predictions = self.predictiondb.get_predictions()
        visuallizer = PredictionVisualizer(predictions,self.phy2)
        visuallizer.write_graphviz(self.outputdir)

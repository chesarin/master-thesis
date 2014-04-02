import logging
from core.phylogeny.phylogenyfactory import PhylogenyFactory
from core.statistics.predictionstats import PredictionStats
from core.plots.xyplot import XyPlot
from core.predictions.predictionsdb import Predictions
from core.predictions.predictionvisualizer import PredictionVisualizer
LOG = logging.getLogger(__name__) 

class Predictor(object):
    #predictor can make predictions by utilizing phylogenies
    def __init__(self, analysisobject, dir1, dir2, iphylogenyfactory, mypredictionmodel, perfectpredictionmodel, outputdir):
        fprintfactory = analysisobject.get_fingerprint_factory()
        distancemetric = analysisobject.get_distance_metric()
        dirfactory = analysisobject.get_directory_factory()
        phy1 = PhylogenyFactory(dir1, dirfactory, fprintfactory, distancemetric, iphylogenyfactory)
        phy2 = PhylogenyFactory(dir2, dirfactory, fprintfactory, distancemetric, iphylogenyfactory)
        self.xyplot = XyPlot()
        self.outputdir = outputdir
        self.phylogeny1 = phy1.get_phylogeny()
        self.phylogeny2 = phy2.get_phylogeny()
        self.predictions = Predictions(self.phylogeny1, self.phylogeny2, mypredictionmodel, perfectpredictionmodel)
        self.predictionsdb = self.predictions.get_predictiondb()
        self.pstats = PredictionStats(self.predictionsdb)
        self.pvisuallizer = PredictionVisualizer(self.predictionsdb, self.phylogeny2)
    def plot_predictions(self):
        x = self.predictionsdb.get_perfect_prediction()
        y = self.predictionsdb.get_my_prediction()
        self.xyplot.set_values(x,y)
        self.xyplot.plot_pdf(self.outputdir)
    def get_statistics(self):
        return self.pstats.get_stats()
    def create_visuallization(self):
        self.pvisuallizer.create_visuallization()
        self.pvisuallizer.write_graphviz(self.outputdir)
    def get_prediction_db(self):
        return self.predictionsdb
    def get_phylogeny1(self):
        return self.phylogeny1

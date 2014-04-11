import logging
import abc
from core.phylogeny.phylogenyfactory import PhylogenyFactory
from core.statistics.predictionstats import PredictionStats
from core.plots.xyplot import XyPlot
from core.predictions.predictionsdb import PredictionsDB
from core.predictions.predictionvisualizer import PredictionVisualizer
LOG = logging.getLogger(__name__) 

class Predictor(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self, analysisobject, dir1, dir2, iphylogenyfactory, mypredictionmodel, perfectpredictionmodel, outputdir):
        fprintfactory = analysisobject.get_fingerprint_factory()
        distancemetric = analysisobject.get_distance_metric()
        dirfactory = analysisobject.get_directory_factory()
        phy1 = PhylogenyFactory(dir1, dirfactory, fprintfactory, distancemetric, iphylogenyfactory)
        phy2 = PhylogenyFactory(dir2, dirfactory, fprintfactory, distancemetric, iphylogenyfactory)
        self.perfect_prediction = None
        self.estimated_prediction = None
        self.pstats = None
        self.predictionsdb = None
        self.pvisuallizer = None
        self.xyplot = XyPlot()
        self.outputdir = outputdir
        self.phylogeny1 = phy1.get_phylogeny()
        self.phylogeny2 = phy2.get_phylogeny()
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
    def create_perfect_prediction(self):
        model = self.ppredictionmodel
        phy1 = self.phylogeny1
        phy2 = self.phylogeny2
        perfect_prediction = model.makePrediction(phy1, phy2)
        self.perfect_prediction = perfect_prediction
    def create_predictions_db(self):
        estimated_pred = self.estimated_prediction
        perfect_pred = self.perfect_prediction
        predictionsdb = PredictionsDB(estimated_pred, perfect_pred)
        predictionsdb.create_predictions()
        self.predictionsdb = predictionsdb
    @abc.abstractmethod
    def create_estimated_prediction():
        pass
    def compute_stats(self):
        stats = PredictionStats(self.predictionsdb)
        self.pstats = stats
    def set_visuallizer(self):
        pvisuallizer = PredictionVisualizer(self.predictionsdb, self.phylogeny2)
        self.pvisuallizer = pvisuallizer
    def create_predictions_db_file(self):
        self.predictionsdb.create_file(self.outputdir)

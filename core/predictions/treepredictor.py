from core.interfaces.ipredictor import Predictor
from core.predictions.prediction.childcountscore import ChildCountScore
from core.predictions.treemodel import TreeModel as PredictionsTreeModel
from core.predictions.perfectpredictions.newdescendantscountfactorypprediction import NewDescendatsCountFactoryPPrediction
from core.phylogeny.trees.treemodel import TreeModel
class TreePredictor(Predictor):
    def __init__(self,analysisobject,dir1,dir2,outdir='/tmp/output'):
        self.scorer = ChildCountScore()
        self.phylogenyfactory = TreeModel()
        self.mypredictionmodel = PredictionsTreeModel()
        self.mypredictionmodel.setScorer(self.scorer)
        self.ppredictionmodel = NewDescendatsCountFactoryPPrediction()
        Predictor.__init__(self, analysisobject, dir1, dir2, self.phylogenyfactory,
                           self.mypredictionmodel, self.ppredictionmodel, outdir)
        
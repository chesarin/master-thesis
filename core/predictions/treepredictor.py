from core.interfaces.ipredictor import Predictor
from core.predictions.prediction.childcountscore import ChildCountScore
from core.predictions.treemodel import TreeModel as PredictionsTreeModel
from core.predictions.treemodel import LinearRegModel, LogisticRegModel, TreeModelClassifier
from core.predictions.prediction.mlscores import LinearRegressionScorer, LogisticRegressionScorer
from core.predictions.perfectpredictions.newdescendantscountfactorypprediction import NewDescendatsCountFactoryPPrediction, NewDescendatsClassifier
from core.phylogeny.trees.treemodel import TreeModel
class TreePredictor(Predictor):
    def __init__(self, analysisobject, dir1, dir2, outdir='/tmp/output'):
        self.scorer = ChildCountScore()
        self.phylogenyfactory = TreeModel()
        self.mypredictionmodel = PredictionsTreeModel()
        self.mypredictionmodel.setScorer(self.scorer)
        self.ppredictionmodel = NewDescendatsCountFactoryPPrediction()
        Predictor.__init__(self, analysisobject, dir1, dir2, self.phylogenyfactory,
                           self.mypredictionmodel, self.ppredictionmodel, outdir)
    def create_estimated_prediction(self):
        model = self.mypredictionmodel
        phy1 = self.phylogeny1
        prediction = model.makePre(phy1)
        self.estimated_prediction = prediction
class TreePredictorClassifier(Predictor):
    def __init__(self, analysisobject, dir1, dir2, outdir='/tmp/output'):
        self.scorer = ChildCountScore()
        self.phylogenyfactory = TreeModel()
        self.mypredictionmodel = TreeModelClassifier()
        self.mypredictionmodel.setScorer(self.scorer)
        self.ppredictionmodel = NewDescendatsClassifier()
        Predictor.__init__(self, analysisobject, dir1, dir2, self.phylogenyfactory,
                           self.mypredictionmodel, self.ppredictionmodel, outdir)
    def create_estimated_prediction(self):
        model = self.mypredictionmodel
        phy1 = self.phylogeny1
        prediction = model.makePre(phy1)
        self.estimated_prediction = prediction
        
class LinearRegTreePredictor(TreePredictor):
    def __init__(self, analysisobject, dir1, dir2, outdir='/tmp/output'):
        self.scorer = LinearRegressionScorer()
        self.phylogenyfactory = TreeModel()
        self.mypredictionmodel = LinearRegModel()
        self.mypredictionmodel.setScorer(self.scorer)
        self.ppredictionmodel = NewDescendatsCountFactoryPPrediction()
        Predictor.__init__(self, analysisobject, dir1, dir2, self.phylogenyfactory,
                           self.mypredictionmodel, self.ppredictionmodel, outdir)

    def create_estimated_prediction(self, theta, num_of_features=1):
        model = self.mypredictionmodel
        model.set_theta(theta)
        phy1 = self.phylogeny1
        prediction = model.makePre(phy1, num_of_features)
        self.estimated_prediction = prediction
class LogisticRegTreePredictor(TreePredictor):
    def __init__(self, analysisobject, dir1, dir2, outdir='/tmp/output'):
        self.scorer = LogisticRegressionScorer() 
        self.phylogenyfactory = TreeModel()
        self.mypredictionmodel = LogisticRegModel()
        self.mypredictionmodel.setScorer(self.scorer)
        self.ppredictionmodel = NewDescendatsClassifier()
        Predictor.__init__(self, analysisobject, dir1, dir2, self.phylogenyfactory,
                           self.mypredictionmodel, self.ppredictionmodel, outdir)
    def create_estimated_prediction(self, theta, num_of_features=1):
        model = self.mypredictionmodel
        model.set_theta(theta)
        phy1 = self.phylogeny1
        prediction = model.makePre(phy1, num_of_features)
        self.estimated_prediction = prediction
            
        
import logging
import sys
from core.interfaces.predictionmodel import PredictionModel
from predictionimpl import PredictionImpl

log = logging.getLogger(__name__)

class TreeModel(PredictionModel):

    def setScorer(self,IScorer):
        self.scorer = IScorer
        self.prediction = PredictionImpl()

    def makePre(self,IPhylogeny):
        log.info('making a prediction')
        # P = PredictionImpl()
        Graph1 = IPhylogeny.get_graph()
        g1nodes = Graph1.nodes()
        scores = {}
        for node in g1nodes:
            scores[node] = self.scorer.computeScore(node,IPhylogeny)
        normalizer = 0
        for svalue in scores.values():
            normalizer += svalue
        log.info('total value of normalizer is %s',str(normalizer))
        for node in g1nodes:
            self.prediction.setPerc(node,round(float(scores[node])/normalizer,3))
        self.prediction.setPercUnrelated(0.0)
        return self.prediction
        
            
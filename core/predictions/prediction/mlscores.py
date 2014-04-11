import logging
from core.interfaces.iscorer import MLScorer
from numpy import exp
LOG = logging.getLogger(__name__)

class LinearRegressionScorer(MLScorer):
    def computeScore(self, thetas, xvalues):
        assert len(thetas) == len(xvalues), 'thetas and xvalues should have same length'
        score = sum(map(lambda i,j:float(i)*float(j), thetas, xvalues))
        return score

class LogisticRegressionScorer(MLScorer):
    def computeScore(self, thetas, xvalues):
        assert len(thetas) == len(xvalues), 'thetas and xvalues should have same length'
        theta_x = sum(map(lambda i,j:float(i)*float(j), thetas, xvalues))
        sigmoid = 1 / (1 + exp(- theta_x))
        LOG.info('sigmoid value is %s', sigmoid)
        score = sigmoid
        LOG.info('score is %s', score)
        return score
        

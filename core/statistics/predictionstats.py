#!/usr/bin/env python
import logging
import rpy2.robjects as robjects
from zope.interface import implements
from core.interfaces.irstats import IRstats
from rpy2.robjects.packages import importr

stats = importr('stats')
log = logging.getLogger(__name__)

class PredictionStats(object):
    implements(IRstats)
    def __init__(self,data):
        log.info('initializing PredictionStats')
        self.ppredictionv = robjects.FloatVector(data.get_perfect_prediction())
        self.mypredictionv = robjects.FloatVector(data.get_my_prediction())
        robjects.globalenv["myprediction"]=self.mypredictionv
        robjects.globalenv["trueprediction"]=self.ppredictionv
        self.mylm = stats.lm( "myprediction ~ trueprediction" )
        self.r = 0.0
        self.m = 0.0
        self.b = 0.0
        log.info('done initializing PredictionStats')
    def _rcoefficient(self):
        log.info('calculating correlation')
        cor = robjects.r['cor']
        self.r = cor(self.ppredictionv,self.mypredictionv)[0]
        log.info('correlation(m) is %s',str(self.r))
    def _slope(self):
        log.info('calculating slope')
        self.m = self.mylm.rx2('coefficients')[1]
        log.info('calculated slope %s',str(self.m))
    def _yintercept(self):
        log.info('calculating y-intercept')
        self.b = self.mylm.rx2('coefficients')[0]
        log.info('yintercept %s',str(self.b))
    def get_stats(self):
        self._rcoefficient()
        self._slope()
        self._yintercept()
        return self.r,self.m,self.b

        





if __name__ == '__main__':
    print 'hello'

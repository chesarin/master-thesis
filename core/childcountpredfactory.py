#!/usr/bin/env python
import os
import logging
from interfaces.itruepredcalc import ITruePredCalc
from predictionimpl import PredictionImpl
log = logging.getLogger(__name__)

class ChildCountPredFactory(ITruePredCalc):

    def makePrediction(self,IPhyl1,IPhyl2):
        P = PredictionImpl()
        Graph1 = IPhyl1.get_graph()
        Graph2 = IPhyl2.get_graph()
        g1nodes = Graph1.nodes()
        S = {}
        for node in g1nodes:
            S[node] = len(Graph1.neighbors(node)) + len(Graph2.neighbors(node))
        X = 0
        for value in S.values():
            X += value
        log.info('total value of X %s',str(X))
        for node in g1nodes:
            log.info('value of S of %s is %s',str(node),str(S[node]))
            P.setPerc(node,float(S[node])/X)
        P.setPercUnrelated(0.0)
        return P
            
        
        
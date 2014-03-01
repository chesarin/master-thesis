#!/usr/bin/env python
import os
import logging
from core.interfaces.itruepredcalc import ITruePredCalc
from core.predictionimpl import PredictionImpl
from core.algorithms.bfs import NewDescendats
log = logging.getLogger(__name__)

class NewDescendatsCountFactoryPPrediction(ITruePredCalc):

    def makePrediction(self,IPhyl1,IPhyl2):
        log.info('starting NewDescendantsCountFactoryPPrediction')
        P = PredictionImpl()
        Graph1 = IPhyl1.get_graph()
        Graph2 = IPhyl2.get_graph()
        g1nodes = Graph1.nodes()
        S = {}
        log.info('trying to find scores based on NewDescendants')
        for node in g1nodes:
            log.info('creating object NewDescendats')
            descendants = NewDescendats(Graph1,Graph2,node)
            log.info('extracting descendatns list from NewDescendants object')
            descendantsList = descendants.getDescendats()
            S[node] = len(descendantsList)
        X = 0
        for value in S.values():
            X += value
        log.info('total value of X %s',str(X))
        for node in g1nodes:
            log.info('value of S of %s is %s',str(node),str(S[node]))
            P.setPerc(node,float(S[node])/X)
        P.setPercUnrelated(0.0)
        return P
            
        
        
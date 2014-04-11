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
class NewDescendatsClassifier(ITruePredCalc):
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
            prediction = 1 if S[node] > 0 else 0
            P.setPerc(node, prediction)
        P.setPercUnrelated(0.0)
        return P

    # def makePrediction(self,IPhyl1,IPhyl2):
    #     log.info('starting NewDescendantsClasssifier')
    #     P = PredictionImpl()
    #     Graph1 = IPhyl1.get_graph()
    #     Graph2 = IPhyl2.get_graph()
    #     g1nodes = Graph1.nodes()
    #     S = {}
    #     log.info('trying to find scores based on NewDescendants')
    #     for node in g1nodes:
    #         log.info('creating object NewDescendats')
    #         descendants = NewDescendats(Graph1,Graph2,node)
    #         log.info('extracting descendatns list from NewDescendants object')
    #         descendantsList = descendants.getDescendats()
    #         S[node] = len(descendantsList)
    #     snode_values = np.array(S.values())
    #     minimum = np.min(snode_values)
    #     maximum = np.max(snode_values)
    #     # X = 0
    #     # for value in S.values():
    #     #     X += value
    #     # log.info('total value of X %s',str(X))
    #     for node in g1nodes:
    #         new_value = (S[node] - minimum)/float(maximum-minimum) 
    #         log.info('value of S of %s is %s',str(node),str(S[node]))
    #         log.info('new value of S of %s is %s', str(node), new_value)
    #         prediction = 0 if new_value < 0.5 else 1
    #         log.info('prediction of S of %s is %s', str(node), prediction)
    #         P.setPerc(node, prediction)
    #     P.setPercUnrelated(0.0)
    #     return P
            
        
        
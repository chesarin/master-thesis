import logging
import sys
from core.interfaces.predictionmodel import PredictionModel
from core.factories.apkfeatures import ApkFeaturesMan
from predictionimpl import PredictionImpl
import numpy as np

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
class TreeModelClassifier(TreeModel):
    def makePre(self,IPhylogeny):
        log.info('making a prediction')
        # P = PredictionImpl()
        Graph1 = IPhylogeny.get_graph()
        g1nodes = Graph1.nodes()
        scores = {}
        for node in g1nodes:
            scores[node] = self.scorer.computeScore(node,IPhylogeny)
        score_values = np.array(scores.values())
        minimum = np.min(score_values)
        maximum = np.max(score_values)
        # normalizer = 0
        # for svalue in scores.values():
        #     normalizer += svalue
        # log.info('total value of normalizer is %s',str(normalizer))
        for node in g1nodes:
            orig_score = scores[node]
            norm_score = (orig_score - minimum) / float( maximum - minimum)
            prediction = 1 if norm_score >= 0.5 else 0
            log.info('orig_score is %s norm_score is %s and prediction is %s',orig_score, norm_score, prediction)
            self.prediction.setPerc(node, prediction)
        self.prediction.setPercUnrelated(0.0)
        return self.prediction
class LinearRegModel(PredictionModel):
    def setScorer(self,IScorer):
        self.scorer = IScorer
        self.prediction = PredictionImpl()
    def set_theta(self, theta):
        self.theta = theta
    def makePre(self, IPhylogeny, num_features=1):
        log.info('making a prediction based on linear regression')
        theta = self.theta
        graph = IPhylogeny.get_graph()
        malware_corpus = IPhylogeny.get_corpus()
        nodes = graph.nodes()
        # print 'iterating over malware corpus'
        actual_malware = {}
        for i in malware_corpus:
            for j in nodes:
                # print i
                # print j
                if str(i) == str(j) and i not in actual_malware:
                    # print 'adding {} item to actual_malware'.format(str(i))
                    actual_malware[i] = j
        # actual_malware = [ j for i,j in zip(nodes,malware_corpus) if str(i) == str(j)]
        log.info('length of malware corpus is %s', malware_corpus.get_size())
        log.info('length of list of nodes is %s', len(nodes))
        log.info('length of actual malware is %s', len(actual_malware))
        scores = {}
        # P = PredictionImpl()
        for malware in actual_malware.keys():
            feat_man = ApkFeaturesMan(malware, graph)
            feat_man.create_features(num_features)
            bias_feature = [1.0]
            extracted_features = list(feat_man.get_features())
            # print bias_feature
            # print extracted_features
            features = bias_feature + extracted_features
            # print theta
            # print features
            scores[str(malware)] = self.scorer.computeScore(theta, features)
        normalizer = 0
        for svalue in scores.values():
            normalizer += svalue
        log.info('total value of normalizer is %s',str(normalizer))
        for malware in actual_malware.keys():
            self.prediction.setPerc(actual_malware[malware],round(float(scores[str(malware)])/normalizer,3))
        self.prediction.setPercUnrelated(0.0)
        return self.prediction
class LogisticRegModel(LinearRegModel):
    def makePre(self, IPhylogeny, num_features=1):
        log.info('making a prediction based on linear regression')
        theta = self.theta
        graph = IPhylogeny.get_graph()
        malware_corpus = IPhylogeny.get_corpus()
        nodes = graph.nodes()
        print 'iterating over malware corpus'
        actual_malware = {}
        for i in malware_corpus:
            for j in nodes:
                # print i
                # print j
                if str(i) == str(j) and i not in actual_malware:
                    # print 'adding {} item to actual_malware'.format(str(i))
                    actual_malware[i] = j
        # actual_malware = [ j for i,j in zip(nodes,malware_corpus) if str(i) == str(j)]
        log.info('length of malware corpus is %s', malware_corpus.get_size())
        log.info('length of list of nodes is %s', len(nodes))
        log.info('length of actual malware is %s', len(actual_malware))
        scores = {}
        # P = PredictionImpl()
        for malware in actual_malware.keys():
            feat_man = ApkFeaturesMan(malware, graph)
            feat_man.create_features(num_features)
            bias_feature = [1.0]
            extracted_features = list(feat_man.get_features())
            print bias_feature
            print extracted_features
            features = bias_feature + extracted_features
            print theta
            print features
            scores[str(malware)] = self.scorer.computeScore(theta, features)
        normalizer = 0
        for svalue in scores.values():
            normalizer += svalue
        for malware in actual_malware.keys():
            orig_value = scores[str(malware)]
            norm_value = 1 if orig_value >= 0.5 else 0 
            self.prediction.setPerc(actual_malware[malware], norm_value)
        self.prediction.setPercUnrelated(0.0)
        return self.prediction
    
            
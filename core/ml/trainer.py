import logging
import time
import os
import csv
import oct2py as op
from numpy import *
import scipy.optimize as opt
from core.factories.apkfeatures import ApkFeaturesMan
from abc import ABCMeta,abstractmethod
LOG = logging.getLogger(__name__)

class Trainer(object):
    __metaclass__ = ABCMeta
    def __init__(self, predictor, malwarecorpus, num_of_features=1):
        LOG.info('initializing trainer')
        self.phylogeny = predictor.get_phylogeny1()
        self.predictionsdb = predictor.get_prediction_db()
        self.trainingset = []
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        self.malwarecorpus = malwarecorpus
        self.num_of_features = num_of_features
        self.X = []
        self.y = []
        self.thetas = []
        LOG.info('done initializing')
    # @abstractmethod
    # def create_training_set(self):
    #     pass
    @abstractmethod
    def calculate_thetas(self):
        pass
    @abstractmethod
    def _create_lookup_table(self):
        pass
    def create_training_set(self):
        # predictionsdb = self.predictionsdb
        num_of_features = self.num_of_features
        lookuptable = {}
        trainingset = []
        training_x = []
        training_y = []
        graph = self.phylogeny.get_graph()
        lookuptable = self._create_lookup_table()
        for malware in self.malwarecorpus:
            feat_man = ApkFeaturesMan(malware, graph)
            feat_man.create_features(num_of_features)
            features = feat_man.get_features()
            training_x.append(features)
            training_y.append(lookuptable[str(malware)])
            trainingentry = (str(malware),) + features + (lookuptable[str(malware)],)
            trainingset.append(trainingentry)
        self.trainingset = trainingset
        LOG.info('calculating thetas')
        LOG.info('length of X is %s and Y is %s',len(training_x), len(training_y))
        # self.calculate_thetas(training_x, training_y)
        self.X = training_x
        self.y = training_y
    def get_trainig_set(self):
        return self.trainingset
    def _create_directory(self, outputdir):
        directory = outputdir + '/ml-trainingsets-results/'
        if not os.path.exists(directory):
            LOG.info('path does not exist so create directory for predictions')
            os.makedirs(directory)
        filename = directory + 'ml-trainingset-'+ self.timestr+'.csv'
        return filename
    def create_trainingset_file(self, outputdir):
        filename = self._create_directory(outputdir)
        header = ['Malware','Permissions','Receivers','DexClasses',
                  'ChildrenNum','AgeFromParent','DistanceFromParent',
                  'NodeAgeFromRoot','NodeAgeFromLatest','AgeLatestChild',
                  'AgeNewestDescendant','PerfectPrediction']
        with open(filename, 'wb') as fp:
            fp_csv = csv.writer(fp)
            fp_csv.writerow(header)
            fp_csv.writerows(self.trainingset)
    def create_phylogeny_file(self, outputdir):
        filename = outputdir + '/ml-trainingsets-results/'+'phylogeny1-' + self.timestr + '.dot'
        graph = self.phylogeny.get_graph()
        graph.write(filename)
    def create_xy_file(self, outputdir):
        xy = [ row[1:len(row)] for row in self.trainingset]
        directory = outputdir + '/ml-trainingsets-results/'
        filename = directory + 'ml-xyvalues-'+ self.timestr+'.csv'
        with open(filename, 'wb') as fp:
            fp_csv = csv.writer(fp)
            fp_csv.writerows(xy)
    def get_thetas(self):
        return self.thetas
        
class LinerRegressionTrainer(Trainer):
    def _create_lookup_table(self):
        predictionsdb = self.predictionsdb
        lookuptable = {}
        for entry in predictionsdb:
            lookuptable[str(entry[0])] = entry[2]
        return lookuptable
    def calculate_thetas(self):
        X = array(self.X, dtype=float)
        Y = array(self.y)
        LOG.info('X rows %s columns %s',X.shape[0], X.shape[1])
        LOG.info('Y rows %s ',Y.shape[0])
        yrows = Y.shape[0]
        LOG.info('the yrows is %s', yrows)
        Y.resize((yrows,1))
        # print X
        # print Y
        LOG.info('Y rows %s columns %s',Y.shape[0], Y.shape[1])
        temp = ones((yrows,1))
        X = hstack((temp,X))
        octave = op.Oct2Py()
        octave.addpath('core/ml')
        octave.put('X', X)
        octave.put('y', Y)
        octave.run("theta = normalEqn(X,y)")
        temp_theta = array(octave.get('theta'))
        self.thetas = temp_theta.ravel().tolist()
        # print self.thetas
class LogisticRegressionTrainer(Trainer):
    def sigmoid(self, X):
        return 1 / (1 + exp(- X))
    def predict(self, theta, X):
        p_1 = self.sigmoid(dot(X, theta))
        return p_1 > 0.5        
    def cost(self, theta, X, y):
        p_1 = self.sigmoid(dot(X, theta)) # predicted probability of label 1
        log_l = (-y)*log(p_1) - (1-y)*log(1-p_1) # log-likelihood vector
        return log_l.mean()
    def grad(self, theta, X, y):
        # print X
        # print theta
        # print 'initial theta {}'.format(theta.shape)
        # print y
        theta.resize((theta.shape[0],1))
        # print theta
        # print 'initial theta {}'.format(theta.shape)
        print 'x shape is {}'.format(X.shape)
        print 'thetat shape is {}'.format(theta.shape)
        print 'y shape  is {}'.format(y.shape)
        p_1 = self.sigmoid(dot(X, theta))
        print 'p1 shape is {}'.format(p_1.shape)
        error = p_1 - y # difference between label and prediction
        grad = dot(error, X) / y.size # gradient vector
        return grad
    def calculate_thetas(self):
        X = array(self.X, dtype=float)
        Y = array(self.y)
        LOG.info('X rows %s columns %s',X.shape[0], X.shape[1])
        LOG.info('Y rows %s ',Y.shape[0])
        yrows = Y.shape[0]
        LOG.info('the yrows is %s', yrows)
        Y.resize((yrows,1))
        LOG.info('Y rows %s columns %s',Y.shape[0], Y.shape[1])
        octave = op.Oct2Py()
        octave.addpath('core/ml/logistic')
        print X
        print Y
        # octave.put('X', X)
        octave.put('y', Y)
        print octave.run('whos')
        # octave.run("[X_norm mu sigma] = featureNormalize(X)")
        # X_norm = array(octave.get('X_norm'))
        # print X_norm
        temp = ones((yrows,1))
        X = hstack((temp, X))
        print X
        print octave.run('whos')
        octave.put('X', X)
        octave.run("theta = logistic(X,y)")
        temp_theta = array(octave.get('theta'))
        self.thetas = temp_theta.ravel().tolist()
        print octave.run('whos')
        print self.thetas
        p = self.predict(temp_theta, X)
        print 'Train Accuracy: %f' % ((Y[where(p == Y)].size / float(Y.size)) * 100.0)
    def calculate_thetas2(self):
        X = array(self.X, dtype=float)
        Y = array(self.y)
        LOG.info('X rows %s columns %s',X.shape[0], X.shape[1])
        LOG.info('Y rows %s ',Y.shape[0])
        yrows = Y.shape[0]
        LOG.info('the yrows is %s', yrows)
        Y.resize((yrows,1))
        LOG.info('Y rows %s columns %s',Y.shape[0], Y.shape[1])
        temp = ones((yrows,1))
        X = hstack((temp,X))
        print X
        print Y
        initial_theta = zeros((X.shape[1],1))
        print 'initial theta {}'.format(initial_theta.shape)
        print initial_theta
        temp_theta = opt.fmin_bfgs(self.cost, initial_theta, fprime=self.grad, args=(X, Y))
        self.thetas = temp_theta.ravel().tolist()
        print self.thetas
        p = self.predict(temp_theta, X)
        print 'Train Accuracy: %f' % ((Y[where(p == Y)].size / float(Y.size)) * 100.0)
    def _create_lookup_table(self):
        predictionsdb = self.predictionsdb
        lookuptable = {}
        for entry in predictionsdb:
            print entry
            temp = 0
            if entry[2] > 0:
                temp = 1
            lookuptable[str(entry[0])] = temp
        return lookuptable
        


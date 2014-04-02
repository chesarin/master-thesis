import logging
import time
import os
import csv
from core.factories.apkfeatures import ApkFeatures
from core.phylogeny.phyfeatures import PhylogenyFeatures
from abc import ABCMeta,abstractmethod
LOG = logging.getLogger(__name__)
class Trainer(object):
    __metaclass__ = ABCMeta
    def __init__(self, predictor, malwarecorpus):
        self.phylogeny = predictor.get_phylogeny1()
        self.predictionsdb = predictor.get_prediction_db()
        self.trainingset = []
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        self.malwarecorpus = malwarecorpus
    @abstractmethod
    def create_training_set(self):
        pass
    def get_trainig_set(self):
        return self.trainingset
    def _create_directory(self, outputdir):
        directory = outputdir + '/ml-trainingsets-results/'
        if not os.path.exists(directory):
            LOG.info('path does not exist so create directory for predictions')
            os.makedirs(directory)
        filename = directory + 'ml-trainingset-'+ self.timestr+'.csv'
        return filename
    def create_file(self, outputdir):
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
        
        
class ApkTrainer(Trainer):
    def __init__(self, predictor, malwarecorpus):
        Trainer.__init__(self, predictor, malwarecorpus)
    def create_training_set(self):
        predictionsdb = self.predictionsdb.get_predictions()
        lookuptable = {}
        trainingset = []
        graph = self.phylogeny.get_graph()
        for entry in predictionsdb:
            lookuptable[str(entry[0])] = entry[2]
        for malware in self.malwarecorpus:
            apk_featureextractor = ApkFeatures(malware)
            apk_featureextractor.create_features()
            phy_featureextractor = PhylogenyFeatures(graph, malware)
            phy_featureextractor.create_features()
            apkfeatures = apk_featureextractor.get_features_values()
            phyfeatures = phy_featureextractor.get_features_values()
            trainingentry = (str(malware),) + apkfeatures + phyfeatures + (lookuptable[str(malware)],)
            trainingset.append(trainingentry)
        self.trainingset = trainingset
            
        
        
        
        
        
    
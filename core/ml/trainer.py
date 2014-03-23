import logging
import time
import os
from core.factories.apkfeatures import ApkFeatures
LOG = logging.getLogger(__name__)
class Trainer(object):
    def __init__(self, predictor, malwarecorpus):
        self.predictionsdb = predictor.get_prediction_db()
        self.trainingset = []
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        self.malwarecorpus = malwarecorpus
    def create_training_set(self):
        pass
        # # predictor = self.predictor
        # predictionsdb = self.predictionsdb.get_predictions()
        # lookuptable = {}
        # trainingset = []
        # for entry in predictionsdb:
        #     lookuptable[entry[0]] = entry[2]
        # for malware in lookuptable.keys():
        #     featureextractor = ApkFeatures(malware)
        #     featureextractor.create_features()
        #     features = featureextractor.get_features()
        #     trainingentry = malware,features,lookuptable[malware]
        #     trainingset.append(trainingentry)
        # self.trainingset = trainingset
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
        header = '{:32}\t{:11}\t{:9}\t{:10}\t{:17}\n'.format('Malware',
                                                      'Permissions',
                                                      'Receivers',
                                                      'DexClasses',
                                                      'PerfectPrediction')
        with open(filename, 'wb') as fp:
            fp.write(header)
            for entry in self.trainingset:
                malware, ft1, ft2, ft3, pprediction = entry
                value = '{:32}\t{:11}\t{:9}\t{:10}\t{:17}\n'.format(str(malware),
                                                             str(ft1),
                                                             str(ft2),
                                                             str(ft3),
                                                             str(pprediction))
                fp.write(value)
                
class ApkTrainer(Trainer):
    def __init__(self, predictor, malwarecorpus):
        Trainer.__init__(self, predictor, malwarecorpus)
    def create_training_set(self):
        # predictor = self.predictor
        predictionsdb = self.predictionsdb.get_predictions()
        lookuptable = {}
        trainingset = []
        # apkfeatures = []
        for entry in predictionsdb:
            lookuptable[str(entry[0])] = entry[2]
        for malware in self.malwarecorpus:
            featureextractor = ApkFeatures(malware)
            featureextractor.create_features()
            features = featureextractor.get_features()
            ft1, ft2, ft3 = features[0][1], features[1][1], features[2][1]
            trainingentry = str(malware), ft1, ft2, ft3, lookuptable[str(malware)]
            trainingset.append(trainingentry)
        self.trainingset = trainingset
    # def 
            
        
        
        
        
        
    
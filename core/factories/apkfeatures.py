from core.interfaces.ifeature import Features
from core.phylogeny.phyfeatures import PhylogenyFeatures
from core.apk.features import DangerousPermissions,NumberReceivers,NumberDexClasses
import logging
LOG = logging.getLogger(__name__)
class ApkFeatures(Features):
    def __init__(self,ApkFile):
        Features.__init__(self,ApkFile)
        self.f1 = DangerousPermissions(self.malware)
        self.f2 = NumberReceivers(self.malware)
        self.f3 = NumberDexClasses(self.malware)
    def create_features(self):
        self.features.append(self.feature_extractor(self.f1))
        self.features.append(self.feature_extractor(self.f2))
        self.features.append(self.feature_extractor(self.f3))
class ApkFeaturesMan(object):
    def __init__(self, malware, graph):
        LOG.info('apkfeaturemanufactorer for malware %s',str(malware))
        self.apkfeatures = ApkFeatures(malware)
        self.phylogenyfeatures = PhylogenyFeatures(graph, malware)
        self.features = []
    def create_features(self, num_of_features=1):
        LOG.info('creating features')
        apkfeatures = self.apkfeatures
        phyfeatures = self.phylogenyfeatures
        apkfeatures.create_features()
        phyfeatures.create_features()
        # bias_feature = [1.0]
        features = apkfeatures.get_features_values() + phyfeatures.get_features_values() 
        LOG.info('length of features array is %s', len(features))
        LOG.info('the number of features requested is %s', num_of_features)
        assert num_of_features <= len(features), 'not a valid value of number of features'  
        self.features = features[0:num_of_features]
        LOG.info('size of self.features is %s', len(self.features))
        # print self.features
    def get_features(self):
        LOG.info('trying to retrieve the following features')
        # print self.features
        return self.features
    # def __iter__(self):
    #     return iter(self.features)
        
import abc
class FeaturesManufacturer(object):
    def __init__(self, malware_corpus, phylogeny_graph):
        self.malware_corpus = malware_corpus
        self.phylogeny_graph = phylogeny_graph
        self.X = []
        self.y = []
    def _create_phylogeny_features(self):
        pass
    def _create_malware_features(self):
        pass
    def create_features_matrix(self):
        self._create_phylogeny_features()
        self._create_phylogeny_features()
class Features(object):
    """Features Factory"""
    __metaclass__ = abc.ABCMeta
    def __init__(self, IMalware):
        self.features = []
        self.malware = IMalware
    def get_features(self):
        return self.features
    def get_features_values(self):
        values_list = [entry[1] for entry in self.features]
        return tuple(values_list)
    def get_num_features(self):
        return len(self.features)
    def feature_extractor(self, f):
        feature = f
        feature.compute_feature()
        featurename = feature.get_name()
        featurevalue = feature.get_value()
        return featurename,featurevalue
    @abc.abstractmethod
    def create_features(self):
        pass
class NumericFeature(object):
    """Feature Interface"""
    __metaclass__ = abc.ABCMeta
    def __init__(self,IMalware,name):
        self.malware = IMalware
        self.name = name
        self.value = 0
    def get_value(self):
        return self.value
    def get_name(self):
        return self.name
    @abc.abstractmethod
    def compute_feature(self):
        pass
class BooleanFeature(object):
    """Feature Interface"""
    __metaclass__ = abc.ABCMeta
    def __init__(self, IMalware):
        self.name = ''
        self.malware = IMalware
        self.value = False
    def get_value(self):
        return self.value
    def get_name(self):
        return self.name
    @abc.abstractmethod
    def compute_feature(self):
        pass
class PhylogenyNumericFeature(object):
    """Features of phylogenies"""
    __metaclass__ = abc.ABCMeta
    def __init__(self, IPhylogeny, IMalware, feature_name):
        self.name = feature_name
        self.phylogeny = IPhylogeny
        self.malware = IMalware
        self.value = 0
    def get_value(self):
        return self.value
    def get_name(self):
        return self.name
    @abc.abstractmethod
    def compute_feature(self):
        pass
    
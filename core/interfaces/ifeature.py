import abc
class Features(object):
    """Features Factory"""
    __metaclass__ = abc.ABCMeta
    def __init__(self, IMalware):
        self.features = []
        self.malware = IMalware
    def get_features(self):
        return self.features
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


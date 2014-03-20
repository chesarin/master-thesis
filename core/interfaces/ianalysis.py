class Analysis(object):
    def __init__(self,IMalwareCorpusFactory,IFingerPrintFactory,IDistanceMetric):
        self.dfactory = IMalwareCorpusFactory
        self.fpf = IFingerPrintFactory
        self.dis = IDistanceMetric
    def get_directory_factory(self):
        return self.dfactory
    def get_distance_metric(self):
        return self.dis
    def get_fingerprint_factory(self):
        return self.fpf

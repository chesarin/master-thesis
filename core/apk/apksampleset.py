from core.interfaces.isampler import SampleSet
from core.apk.apkdirectoryfactory import APKDirectoryFactory

class ApkSampleSet(SampleSet):
    """
    """
    
    def __init__(self, inputdir):
        """
        """
        self.apkdirfactory = APKDirectoryFactory()
        self.apkdirfactory.create(inputdir)
        mc = self.apkdirfactory.get_corpus()
        SampleSet.__init__(self, mc)

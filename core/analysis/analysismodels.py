from core.interfaces.ianalysis import Analysis
from core.dmetrics.ratcliffmetric import RatcliffMetric
from core.apk.apkdirectoryfactory import APKDirectoryFactory
from core.fingerprints.androidmanifestfingerprintfactory import AndroidManifestFingerPrintFactory
class ManifestAnalysis(Analysis):
    def __init__(self):
        self.dfactory = APKDirectoryFactory()
        self.fpf = AndroidManifestFingerPrintFactory()
        self.dis = RatcliffMetric()
    
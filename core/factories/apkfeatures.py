from core.interfaces.ifeature import Features
from core.apk.features import DangerousPermissions,NumberReceivers,NumberDexClasses
class ApkFeatures(Features):
    def __init__(self,ApkFile):
        Features.__init__(self,ApkFile)
    def create_features(self):
        f1 = DangerousPermissions(self.malware)
        f2 = NumberReceivers(self.malware)
        f3 = NumberDexClasses(self.malware)
        self.features.append(self.feature_extractor(f1))
        self.features.append(self.feature_extractor(f2))
        self.features.append(self.feature_extractor(f3))
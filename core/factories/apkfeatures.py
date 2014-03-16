from core.interfaces.ifeature import Features
from core.apk.features import DangerousPermissions,NumberReceivers,NumberDexClasses
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
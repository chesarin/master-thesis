from interfaces.ifingerprintfactory import IFingerPrintFactory
from losslessfingerprint import LosslessFingerPrint

class LosslessFingerPrintFactory(IFingerPrintFactory):
	
	def create(self,imalware):
		self.factory = LosslessFingerPrint(imalware)
		return self.factory

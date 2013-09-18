from interfaces.ifingerprintfactory import IFingerPrintFactory
from androidmanifestfingerprint import AndroidManifestFingerPrint

class AndroidManifestFingerPrintFactory(IFingerPrintFactory):
	
	def create(self,imalware):
		self.factory = AndroidManifestFingerPrint(imalware)
		return self.factory

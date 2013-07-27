#!/usr/bin/env python
from interfaces.ifingerprint import IFingerPrint
class LosslessFingerPrint(IFingerPrint):

	def __init__(self,imalware):
		self.malware = imalware

	def get_malware():
		return self.malware

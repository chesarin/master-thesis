import abc

class IFingerPrintFactory(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def create(self,IMalware):
		"""Return an IFingerPrint object from the input IMalware"""
		return

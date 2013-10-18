import abc

class IDivCalc(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def calcDiv(self,IPred1,IPred2):
		"""Return the distance as a double. f1 and f2 are 
		ifingerprint objects"""
		return

import abc

class IDistanceMetric(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def distance(self,f1,f2):
		"""Return the distance as a double. f1 and f2 are 
		ifingerprint objects"""
		return

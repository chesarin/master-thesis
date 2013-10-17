import abc

class ITruePredCalc(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def makePrediction(self,IPhyl1,IPhyl2):
		"""Return the distance as a double. f1 and f2 are 
		ifingerprint objects"""
		return

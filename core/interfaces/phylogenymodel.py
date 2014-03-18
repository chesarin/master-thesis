import abc

class PhylogenyModel(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def create(self,malwarecorpus,fingerprintfactory,distancemetric):
		"""This will create a PhylogenyModel"""
		return
		

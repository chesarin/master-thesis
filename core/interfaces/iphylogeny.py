import abc

class IPhylogeny(object):

	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def set_corpus(self,imalwarecorpus):
		"""Set the courpus based on the 
		malwarecorpus which is passed as
		a parameter."""
		return

	@abc.abstractmethod
	def add_edge(self,ancestor,descendent,distance):
		"""Adds an edge to the Phylogeny
		currently created."""
		return
		
	# @abc.abstractmethod
	# def write_graphiz_file(self,path):
	# 	"""Create a graphiz file for 
	# 	visuallization."""
	# 	return

	@abc.abstractmethod
	def get_corpus(self):
		"""Return the malware
		corpus."""
		return

	# @abc.abstractmethod
	# def is_edge(self,malwareu,malwarev):
	# 	"""Return true if malwareu
	# 	and malwarev are an edge is this
	# 	phiology."""
	# 	return

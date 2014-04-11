import abc

class IScorer(object):

    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def computeScore(self,IMalware,IPhylogeny):
        """Set a percentage as a double for this malware."""
        return

class MLScorer(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def computeScore(thetas, Xvalues):
        """Compute y value based on theta values and Xvalues
        These values should be obtained via machine learning
        """
        return

import abc

class IScorer(object):

    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def computeScore(self,IMalware,IPhylogeny):
        """Set a percentage as a double for this malware."""
        return

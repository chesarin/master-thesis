import abc

class IModel(object):

    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def setScorer(self,IScorer):
        """Set a percentage as a double for this malware."""
        return
        
    @abc.abstractmethod
    def makePre(self,IPhylogeny):
        """Return a prediction based on the phylogeny passed
        The prediction can be made on graphs or trees."""
        return
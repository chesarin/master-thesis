import abc

class IPredictionFactory(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(self,iphylogeny):
        """Create an prediction using a phylogeny object"""
        return

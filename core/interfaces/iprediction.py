import abc

class IPrediction(object):

    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def setPerc(self,IMalware,percentage):
        """Set a percentage as a double for this malware."""
        return
        
    @abc.abstractmethod
    def setPercUnrelated(self,double):
        """Set a percentage as a double for this malware."""
        return

    @abc.abstractmethod
    def getPerc(self,IMalware):
        """Return double for this percentage."""
        return
        
    @abc.abstractmethod
    def getPercUnrelated(self):
        """Return double for this percentage."""
        return

    @abc.abstractmethod
    def getKeys(self):
        """Get the fertility of a malware."""
        return

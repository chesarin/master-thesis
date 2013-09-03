import abc

class IPrediction(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_percentage_unrelated(self):
        """Return double for this percentage."""
        return

    @abc.abstractmethod
    def get_fertility(self,imalware):
        """Get the fertility of a malware."""
        return

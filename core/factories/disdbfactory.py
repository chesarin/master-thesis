"""disdbfactory module"""
import logging
from core.dmetrics.disdb import DisDB

LOG = logging.getLogger(__name__)


class DisDBFactory(object):
    """DisDBFactory class creates DisDB objects"""
    def __init__(self, inputdir, metric, fpfactory, dfactory):
        """default contructor"""
        self.disdb = DisDB(inputdir, metric, fpfactory, dfactory)
        # return self.disdb
    def create(self):
        """create method that returns a disdb object"""
        # self.disdb = DisDB(inputdir, metric, fpfactory, dfactory)
        return self.disdb

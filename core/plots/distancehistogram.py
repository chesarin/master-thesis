"""distancehistogram module"""
from core.plots.histogram import Histogram
import logging

LOG = logging.getLogger(__name__)

class DistanceHistogram(object):
    """DistanceHistogram class"""
    def __init__(self, disdb):
        """Constructor takes disdbfactory to plot in histogram"""
        self.disdb = disdb.get_distances()
        self.histogram = None
    def create(self):
        self.histogram = Histogram(self.disdb)
        return self.histogram

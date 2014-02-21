#!/usr/bin/env python
from zope.interface import Interface
class IRstats(Interface):
    """Interface for statistics using R"""
    def __init__(data):
        """IRstats constructor takes the data to be used for calculations"""
    def _rcoefficient():
        """Calculates correlation coefficient"""
    def _slope():
        """Calculates slope"""
    def _yintercept():
        """Calculates yintercept"""
    def get_stats():
        """Return a tuple with slope,y-intercept,correlation coefficient"""
#!/usr/bin/env python
"""Rplot base class to create plot objects based on R"""
import abc
class Rplot(object):
    """Interface for plotting data using R"""
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __init__(self):
        """Constructor of Rplot."""
        return
    @abc.abstractmethod
    def plot_pdf(self, outputdir):
        """Create pdf file on the outputdirectory specified"""
        pass
            
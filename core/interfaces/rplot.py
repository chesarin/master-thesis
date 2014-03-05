#!/usr/bin/env python
import abc
class Rplot(object):
    """Interface for plotting data using R"""
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def __init__(data): pass
    
    @abc.abstractmethod
    def pdfPlot(outputdir): pass
            
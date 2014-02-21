#!/usr/bin/env python
from zope.interface import Interface
class IRplot(Interface):
    """Interface for plotting data using R"""
    def __init__(data):
        """IRplot constructor takes the data to be used for graph"""
    def pdfPlot(outputdir):
        """pdfplot creates a PDF file it takes as an argument an outputdirectory"""
        
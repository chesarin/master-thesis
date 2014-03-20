#!/usr/bin/env python
"""XyPlot module"""
import logging
import time
import os
import rpy2.robjects as robjects
from core.interfaces.rplot import Rplot
from rpy2.robjects.packages import importr

stats = importr('stats')
log = logging.getLogger(__name__)


class XyPlot(Rplot):
    """XyPlot class to plot xy-graphs"""
    def __init__(self, x=[0.0], y=[0.0]):
        """Constructor takes a array of floats for x and y coordinates"""
        log.info('initializing Xyplot')
        self.x = robjects.FloatVector(x)
        self.y = robjects.FloatVector(y)
    def _check_dir(self, outdir):
        """_checkDir will check if output directory exists"""
        directory = outdir + '/xy-plot/'
        log.info('checking if directory exists')
        if not os.path.exists(directory):
            log.info('%s does not exist so create directory', directory)
            os.makedirs(directory)
        return directory
    def _create_file(self, outdir):
        """createFile will create an output file with a timestamp"""
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = outdir + 'xyscatter-' + timestr + '.pdf'
        return filename
    def set_values(self,x,y):
        self.x = robjects.FloatVector(x)
        self.y = robjects.FloatVector(y)
    def plot_pdf(self, outdir='output'):
        """will plot graph as a pdf"""
        log.info('starting pdf plot')
        directory = self._check_dir(outdir)
        filename = self._create_file(directory)
        grdevices = importr('grDevices')
        grdevices.pdf(file=filename)
        x = self.x
        y = self.y
        robjects.globalenv["x"] = x
        robjects.globalenv["y"] = y
        r = robjects.r
        r.plot(x, y, xlab="True Prediction",
               ylab="My Prediction", pch=8,
               col="blue")
        r.abline(r.lm("y~x"), col="red")
        grdevices.dev_off()
        log.info('done plotting pdf file %s', filename)




        

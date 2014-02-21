#!/usr/bin/env python
import logging
import time
import os
import rpy2.robjects as robjects
from zope.interface import implements
from core.interfaces.irplot import IRplot
from rpy2.robjects.packages import importr

stats = importr('stats')
log = logging.getLogger(__name__)


class XyPlot(object):
    implements (IRplot)
    def __init__(self,data):
        log.info('initializing Xyplot')
        self.x = robjects.FloatVector(data.get_perfect_prediction())
        self.y = robjects.FloatVector(data.get_my_prediction())
    def _checkDir(self,outdir):
        directory = outdir + '/xy-plot/'
        log.info('checking if directory exists')
        if not os.path.exists(directory):
            log.info('%s does not exist so create directory',directory)
            os.makedirs(directory)
        return directory
    def _createFile(self,outdir):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = outdir + 'xyscatter-' + timestr + '.pdf'
        return filename
    def pdfPlot(self,outdir='output'):
        log.info('starting pdf plot')
        directory = self._checkDir(outdir)
        filename = self._createFile(directory)
        grdevices = importr('grDevices')
        grdevices.pdf(file=filename)
        x = self.x
        y = self.y
        robjects.globalenv["x"] = x
        robjects.globalenv["y"] = y
        r = robjects.r
        r.plot(x,y,xlab="True Prediction",ylab="My Prediction",pch=8,col="blue")
        r.abline(r.lm("y~x"),col="red")
        grdevices.dev_off()
        log.info('done plotting pdf file %s',filename)




        

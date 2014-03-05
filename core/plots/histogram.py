#!/usr/bin/env python
"""histogram module"""
import logging
import time
import os
import rpy2.robjects as robjects
from core.interfaces.rplot import Rplot
from rpy2.robjects.packages import importr

stats = importr('stats')
log = logging.getLogger(__name__)


class Histogram(Rplot):
    """Histogram class to plot Histograms"""
    def __init__(self, data):
        """constructor takes the data to plot"""
        log.info('initializing histogram')
        self.x = robjects.FloatVector(data.getData())
    def _check_dir(self, outdir):
        """Will check that outputdir exists"""
        directory = outdir + '/histogram/'
        log.info('checking if directory exists')
        if not os.path.exists(directory):
            log.info('%s does not exist so create directory', directory)
            os.makedirs(directory)
        return directory
    def _create_file(self, outdir):
        """Will create file with specific date"""
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = outdir + 'histogram-' + timestr + '.pdf'
        return filename
    def plot_pdf(self, outdir='output'):
        """Will plot graph in pdf format"""
        log.info('starting pdf plot')
        directory = self._check_dir(outdir)
        filename = self._create_file(directory)
        grdevices = importr('grDevices')
        grdevices.pdf(file=filename)
        x = self.x
        r = robjects.r
        bins = robjects.FloatVector([0.0, 0.25, 0.50, 0.75, 1.0])
        r.hist(x, breaks=bins)
        grdevices.dev_off()
        log.info('done plotting pdf file %s', filename)




        

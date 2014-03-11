#!/usr/bin/env python
"""histogram module"""
import logging
import time
import os
import rpy2.robjects as robjects
from core.interfaces.rplot import Rplot
from rpy2.robjects.packages import importr

stats = importr('stats')
LOG = logging.getLogger(__name__)


class Histogram(Rplot):
    """Histogram class to plot Histograms"""
    def __init__(self, inputlist):
        """constructor takes the data to plot"""
        LOG.info('initializing histogram')
        self.timestr = None
        self.x = robjects.FloatVector(inputlist)
    def _check_dir(self, outdir):
        """Will check that outputdir exists"""
        directory = outdir + '/histogram/'
        LOG.info('checking if directory exists')
        if not os.path.exists(directory):
            LOG.info('%s does not exist so create directory', directory)
            os.makedirs(directory)
        return directory
    def _create_file(self, outdir):
        """Will create file with specific date"""
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = outdir + 'histogram-' + self.timestr + '.pdf'
        return filename
    def plot_pdf(self, outdir='output'):
        """Will plot graph in pdf format"""
        LOG.info('starting pdf plot')
        directory = self._check_dir(outdir)
        filename = self._create_file(directory)
        grdevices = importr('grDevices')
        grdevices.pdf(file=filename)
        x = self.x
        r = robjects.r
        bins = robjects.FloatVector([0.0, 0.25, 0.50, 0.75, 1.0])
        r.hist(x, breaks=bins,main=self.timestr,xlab='Distance')
        grdevices.dev_off()
        LOG.info('done plotting pdf file %s', filename)




        

#!/usr/bin/env python
"""
PredictionVisualizer module
"""
import time
import os
import logging

LOG = logging.getLogger(__name__)
class PredictionVisualizer(object):
    """
    PredictionVisualizer class
    """
    def __init__(self, predictiondb, realphylogeny):
        LOG.info('initializing')
        self.predictiondb = predictiondb
        self.phylogenygraph = realphylogeny.get_graph()
        self._set_phylogeny_color()
    def _set_phylogeny_color(self):
        LOG.info('setting color of nodes according to predictions values')
        for entry in self.predictiondb:
            malware,myprediction,trueprediction = entry
            LOG.info('malware = %s',str(malware))
            LOG.info('myprediction = %s trueprediction = %s',
                     str(myprediction),
                     str(trueprediction))
            node = self.phylogenygraph.get_node(malware)
            if myprediction < trueprediction:
                LOG.info('%s was underestimated', str(node))
                node.attr['color'] = 'red'
            elif myprediction > trueprediction:
                LOG.info('%s was overestimated', str(node))
                node.attr['color'] = 'blue'
            elif myprediction == trueprediction:
                LOG.info('%s was on point',str(node))
                node.attr['color'] = 'green'
                
    def _create_directory_and_filename(self, directory, name):
        LOG.info('creating directory if not present and return filename')
        timestr = time.strftime("%Y%m%d-%H%M%S")
        directory = directory + '/graphviz/'
        if not os.path.exists(directory):
            LOG.info('path does not exist so create directory for predictions')
            os.makedirs(directory)
        filename = directory + name + '-' + timestr + '.dot'
        return filename
        
    def write_graphviz(self, outputdir='output', name='truephylogeny'):
        LOG.info('creating graphviz file of true prediction')
        filename = self._create_directory_and_filename(outputdir, name)
        self.phylogenygraph.write(filename)    

import logging
import time
import os
from apkdirectoryfactory import APKDirectoryFactory

log = logging.getLogger(__name__)

class DisDB(object):
    def __init__(self,directory,metric,fprintfactory,outputdir='output'):
        """Test"""
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        self.fpfactory = fprintfactory
        self.directory = directory
        self.distances = []
        self.metric = metric
        self.dfactory = APKDirectoryFactory()
        self.dfactory.create(directory)
        self.mc = self.dfactory.get_corpus()
        self.outputdir = outputdir
    def create_file(self):
        """Create file of distances"""
        header = '{:32}\t{:32}\t{:14}\n'.format('MalwareA','MalwareB','Distance')
        directory = self.outputdir + '/distance/'
        if not os.path.exists(directory):
            log.info('path does not exist so create directory')
            os.makedirs(directory)
        filename = directory + 'distances-' + self.timestr+'.txt' 
        with open(filename,'wb') as fp:
            fp.write(header)
            for i in range(self.mc.get_size()):
                a = self.mc.getNthCronological(i)
                for j in range(self.mc.get_size()):
                    b = self.mc.getNthCronological(j)
                    dis = self.metric.distance(self.fpfactory.create(a),
                                               self.fpfactory.create(b))
                    self.distances.append(dis)
                    log.info('a %s b %s distance %s',str(a),str(b),str(dis))
                    value = str(a)+"\t "+str(b)+"\t"+str(dis)+"\n"
                    fp.write(value)
    def get_distances(self):
        """Return the distances list"""
        log.info('obtaining distances')
        return self.distances


"""DisDBclass to store distances of malware"""
import logging

LOG = logging.getLogger(__name__)

class DisDB(object):
    """DisDB will store a list with all the distances of malware"""
    def __init__(self, inputdir, metric, fprintfactory, dfactory):
        """Constructors needs the following:
        inputdir=directory of malware to read from
        metric=we need a distance metric to calculate the distances
        fprintfactory=a fingerprint factory to create fingerprints
        dfactory=to create a factory to extract malware from"""
        self.distancedb = []
        self.fpfactory = fprintfactory
        self.inputdir = inputdir
        self.metric = metric
        self.dfactory = dfactory
        self.dfactory.create(self.inputdir)
        self.malwarecorpus = self.dfactory.get_corpus()
        self._create_db()
    def _create_db(self):
        """Store distances as tuples with the following
        (malware1,malware2,distance)"""
        # self.outputdir = outputdir
        # header = '{:32}\t{:32}\t{:14}\n'.format('MalwareA',
        #'MalwareB','Distance')
        # directory = self.outputdir + '/distance/'
        # if not os.path.exists(directory):
        #     LOG.info('path does not exist so create directory')
        #     os.makedirs(directory)
        # filename = directory + 'distances-' + self.timestr+'.csv' 
        # with open(filename,'wb') as fp:
        #     fp.write(header)
        for i in range(self.malwarecorpus.get_size()):
            mal1 = self.malwarecorpus.getNthCronological(i)
            for j in range(self.malwarecorpus.get_size()):
                mal2 = self.malwarecorpus.getNthCronological(j)
                if not mal1 == mal2:
                    dis = self.metric.distance(self.fpfactory.create(mal1),
                                               self.fpfactory.create(mal2))
                    entry = mal1, mal2, dis
                    self.distancedb.append(entry)
                    LOG.info('mal1 %s mal2 %s distance %s',
                             str(mal1), str(mal2), str(dis))
                # self.distances.append(dis)

                # value = str(a)+"\t "+str(b)+"\t"+str(dis)+"\n"
                # fp.write(value)
    def get_distances(self):
        """Return the distances list"""
        LOG.info('obtaining distances')
        distances = [entry[2] for entry in self.distancedb]
        return distances

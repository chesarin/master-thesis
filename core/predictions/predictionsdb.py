import logging
import time
import os

log = logging.getLogger(__name__)


class PredictionsDB(object):
    def __init__(self, pred1, pred2):
        self.prediction1 = pred1
        self.prediction2 = pred2
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        self.predictionsdb = []
    def create_predictions(self):
        db = self.prediction1.getKeys()
        for malware in db:
            myprediction = self.prediction1.getPerc(malware)
            pprediction = self.prediction2.getPerc(malware)
            entry = malware,myprediction,pprediction
            self.predictionsdb.append(entry)
    def _create_directory(self, outputdir):
        directory = outputdir + '/predictions/'
        if not os.path.exists(directory):
            log.info('path does not exist so create directory for predictions')
            os.makedirs(directory)
        filename = directory + 'predictions-'+ self.timestr+'.csv'
        return filename
    def create_file(self, outputdir='output'):
        filename = self._create_directory(outputdir)
        header = '{:3}\t{:32}\t{:12}\t{:15}\n'.format('ID',
                                                      'Malware',
                                                      'TruePrediction',
                                                      'MyPrediction')
        with open(filename, 'wb') as fp:
            fp.write(header)
            for entry in self.predictionsdb:
                malware,myprediction,pprediction = entry
                mid = malware.attr['label']
                value = '{:3}\t{:32}\t{:12}\t{:15}\n'.format(str(mid),
                                                             str(malware),
                                                             str(pprediction)[:6],
                                                             str(myprediction))
                fp.write(value)
                log.info('%s %s %s %s',
                         str(mid),
                         str(malware),
                         str(pprediction),
                         str(myprediction))
    def get_my_prediction(self):
        return [ entry[1] for entry in self.predictionsdb]
    def get_perfect_prediction(self):
        return [ entry[2] for entry in self.predictionsdb ]
    def get_predictions(self):
        return self.predictionsdb
    def __iter__(self):
        return iter(self.predictionsdb)

class Predictions(object):
    def __init__(self, phylogeny1, phylogeny2, mypredictionmodel, ppredictionmodel):
        self.myprediction = mypredictionmodel.makePre(phylogeny1)
        self.perfectprediction = ppredictionmodel.makePrediction(phylogeny1, phylogeny2)
        self.predictionsdb = PredictionsDB(self.myprediction, self.perfectprediction)
        self.predictionsdb.create_predictions()
    def get_predictiondb(self):
        return self.predictionsdb
        
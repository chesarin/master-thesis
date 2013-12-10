import logging
import time
import os

log = logging.getLogger(__name__)


class PredictionsDB(object):
    def __init__(self,pred1,pred2):
        self.prediction1 = pred1
        self.prediction2 = pred2
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        
    def create_file(self,outputdir='output'):
        db = self.prediction1.getKeys()
        directory = outputdir + '/predictions/'
        if not os.path.exists(directory):
            log.info('path does not exist so create directory for predictions')
            os.makedirs(directory)
        filename = directory + 'predictions-'+ self.timestr+'.txt'
        self.mprediction = []
        self.actualprediction = []
        header = '{:32}\t{:12}\t{:15}\n'.format('Malware','MyPrediction','TruePrediction')
        with open(filename,'wb') as fp:
            fp.write(header)
            for malware in db:
                myprediction = self.prediction1.getPerc(malware)
                pprediction = self.prediction2.getPerc(malware)
                self.mprediction.append(myprediction)
                self.actualprediction.append(pprediction)
                value = '{:32}\t{:12}\t{:15}\n'.format(str(malware),str(myprediction)[:6],str(pprediction))
                # value = str(malware)+" \t"+str(myprediction)[:6]+" \t"+str(pprediction)+"\n"
                fp.write(value)
                log.info('%s %s %s',
                         str(malware),
                         str(myprediction),
                         str(pprediction))
    def get_my_prediction(self):
        return self.mprediction
    def get_perfect_prediction(self):
        return self.actualprediction
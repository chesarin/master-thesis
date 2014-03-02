import logging
from core.interfaces.iprediction import IPrediction

log = logging.getLogger(__name__)

class PredictionImpl(IPrediction):
    
    def __init__(self):
        log.info('creating predition')
        self.percentageUnrelated = 0
        self.fertilities = {}

    def setPerc(self,IMalware,percentage):
        log.info('setting Percentage')
        log.info('malware %s',str(IMalware))
        log.info('percentage %s',str(percentage))
        self.fertilities[IMalware] = percentage
        
    def setPercUnrelated(self,percentage):
        log.info('setting percentage unrelated')
        log.info('percentage %s',str(percentage))
        self.percentageUnrelated = percentage

    def getPerc(self,IMalware):
        return self.fertilities[IMalware]
        
    def getPercUnrelated(self):
        return self.percentageUnrelated

    def getKeys(self):
        return self.fertilities.keys()
        
    def print_entries(self):
        log.info('%s %s','percentageunrelated',str(self.percentageUnrelated))
        for i in self.fertilities:
            log.info('malware %s number of children %s',
                     i,str(self.fertilities[i]))
import logging
from interfaces.iprediction import IPrediction

log = logging.getLogger(__name__)

class PredictionImpl(IPrediction):
    
    def __init__(self):
        self.percentageUnrelated = 0
        self.fertilities = {}

    def set_percentage_unrelated(self,percentage):
        self.percentageUnrelated = percentage

    def set_fertility(self,malware,fertility):
        self.fertilities[malware] = fertility
        
    def get_percentage_unrelated(self):
        return self.percentageUnrelated

    def get_fertility(self,imalware):
        return self.fertilities[imalware]

    def print_entries(self):
        log.info('%s %s','percentageunrelated',str(self.percentageUnrelated))
        for i in self.fertilities:
            log.info('malware %s number of children %s',
                     i,str(self.fertilities[i]))
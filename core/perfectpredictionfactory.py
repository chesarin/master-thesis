import logging
from interfaces.ipredictionfactory import IPredictionFactory
from predictionimpl import PredictionImpl

log = logging.getLogger(__name__)

class PerfectPredictionFactory(IPredictionFactory):
    
    def create(self,phylogeny1,phylogeny2):
        log.info('starting')
        self.prediction = PredictionImpl()
        self.prediction.set_percentage_unrelated(0)
        malwarec = phylogeny1.get_corpus()
        for location in range(malwarec.get_size()):
            malware = malwarec.getNthCronological(location)
            self.prediction.set_fertility(malware,
                                          phylogeny1.get_number_of_children(malware))
        self.prediction.print_entries()
        log.info('ending')

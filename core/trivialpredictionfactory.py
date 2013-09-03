from interfaces.ipredictionfactory import IPredictionFactory
from predictionimpl import PredictionImpl

class TrivialPredictionFactory(IPredictionFactory):

    def create(self,phylogeny):
        self.prediction = PredictionImpl()
        self.prediction.set_percentage_unrelated(0)
        malwarec = phylogeny.get_corpus()
        for location in range(malwarec.get_size()):
            self.prediction.set_fertility(malwarec.getNthCronological
                                          [location],0)
        

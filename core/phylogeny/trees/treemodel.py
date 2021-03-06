from core.interfaces.phylogenymodel import PhylogenyModel
from core.phylogeny.graphs.ramresidentgraph import RAMResidentGraph
class TreeModel(PhylogenyModel):

    def create(self,malwarecorpus,fingerprintfactory,distancemetric):
        self.RRG = RAMResidentGraph()
        self.RRG.set_corpus(malwarecorpus)
        self.RRG.create_corpus_hash()
        for i in range(1,malwarecorpus.get_size()):
            m = malwarecorpus.getNthCronological(i)
            mins = float('infinity')
            for j in range(i):
                m2 = malwarecorpus.getNthCronological(j)
                s = distancemetric.distance(fingerprintfactory.create(m),
                                            fingerprintfactory.create(m2))
                if s < mins:
                    mins = s
                    x = m2
            self.RRG.add_edge(x,m,mins)
        return self.RRG

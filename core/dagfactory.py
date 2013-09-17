from interfaces.iphylogenyfactory import IPhylogenyFactory
from ramresidentgraph import RAMResidentGraph
class DAGFactory(IPhylogenyFactory):

    def __init__(self,threshold):
        self.threshold = threshold
    
    def create(self,malwarecorpus,fingerprintfactory,distancemetric):
        self.RRG = RAMResidentGraph()
        self.RRG.set_corpus(malwarecorpus)

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
            if mins < self.threshold:
                self.RRG.add_edge(x,m,mins)
            else:
                self.RRG.add_node(x)
                self.RRG.add_node(m)
        return self.RRG

from interfaces.iphylogenyfactory import IPhylogenyFactory
from ramresidentgraph import RAMResidentGraph
class TreeFactory(IPhylogenyFactory):

	def create(self,malwarecorpus,fingerprintfactory,distancemetric):
		self.RRG = RAMResidentGraph()
		self.RRG.set_corpus(malwarecorpus)

		for i in range(1,malwarecorpus.get_size()):
			m = malwarecorpus.getNthCronological(i)
			mins = float('infinity')
			for j in range(i):
				m2 = malwarecorpus.getNthCronological(j)
				s = distancemetric.distance2(fingerprintfactory.create(m),
											 fingerprintfactory.create(m2))
				if s < mins:
					mins = s
					x = m2
			self.RRG.add_edge(x,m,s)
		self.RRG.print_edges()
		return self.RRG

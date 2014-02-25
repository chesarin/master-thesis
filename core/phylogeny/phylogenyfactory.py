import logging

from phylogeny import Phylogeny

log = logging.getLogger(__name__) 

class PhylogenyFactory(object):
    def __init__(self,inputdir,dfactory,fpfactory,dmetric,phylogenytype):
        self.phylogeny = Phylogeny(inputdir,dfactory,fpfactory,dmetric,phylogenytype)
    def get_phylogeny(self):
        return self.phylogeny.get_core()
                
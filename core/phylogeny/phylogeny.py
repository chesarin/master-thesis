import logging

log = logging.getLogger(__name__) 

class Phylogeny(object):
    def __init__(self,inputdir,dfactory,fpfactory,dmetric,phylogenytype):
        self.dfactory = dfactory
        self.inputdir = inputdir
        self.dmetric = dmetric
        self.dfactory.create(self.inputdir)
        self.mc = self.dfactory.get_corpus()
        self.fpf = fpfactory
        self.phylogenytype = phylogenytype
        self.phylogeny = self.phylogenytype.create(self.mc,self.fpf,self.dmetric)
    def get_core(self):
        return self.phylogeny
    def get_malware_corpus(self):
        return self.mc

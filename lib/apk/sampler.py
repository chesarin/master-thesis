import logging
import random
import time
import os
import shutil
from dateutil.relativedelta import relativedelta

from datetime import datetime

log = logging.getLogger(__name__)

class Sampler(object):
    def __init__(self,winsize=1,samplesize=20,startdate=datetime.today(),outdir='output'):
        log.info('initializing sampler')
        self.winsize = winsize
        self.samplesize = samplesize
        self.startdate = startdate
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.dir1 = outdir +"/set1-"+ self.timestr
        self.dir2 = outdir + "/set2-"+ self.timestr
        self.outdir = outdir
        log.info('done initializing')
        
    def setDb(self,db):
        log.info('setting db')
        self.db = db
        log.info('done setting db')
        
    def extract(self):
        log.info('starting extract process')
        log.info('startdate %s',str(self.startdate))
        log.info('window size is %s',str(self.winsize))
        # log.info('type of %s',dir(self.startdate))
        completion = self.db.get_last_item().get_date()
        log.info('completion %s',str(completion))
        while self.startdate < completion: 
            log.info('startdate %s',str(self.startdate))
            samplex = []
            sampley = []
            datetw = self.startdate + relativedelta(months=+self.winsize)
            datetw2 = self.startdate + relativedelta(months=+(2*self.winsize))
            log.info('datetw %s datetw2 %s',str(datetw),str(datetw2))
            for malware in self.db:
                mdate = malware.get_date()
                if mdate >= self.startdate and mdate < datetw:
                    samplex.append(malware)
                    
            for malware in self.db:
                mdate = malware.get_date()
                if mdate >= datetw and mdate < datetw2:
                    sampley.append(malware)
                
            log.info('samplex size %s',len(samplex))
            log.info('sampley size %s',len(sampley))
            self.startdate += relativedelta(months=self.winsize)
            if len(samplex) != 0 and len(sampley) != 0:
                log.info('sets are not zero, we can move on create two directories and called big program')
                log.info('size of samplex %s',len(samplex))
                log.info('size of sampley %s',len(sampley))
                log.info('size of samplesize %s',self.samplesize)
                try:
                    self.create_directories(samplex,sampley,self.samplesize)
                    #execute is imported from the controller.
                    #controller resides in the main directory
                    execute(self.dir1,self.dir2,self.outdir)
                except Exception as e:
                    log.info('Error creating sample directories')
                    log.info('Reason: %s',str(e))
            log.info('startdate %s',str(self.startdate))
    def create_directories(self,sample1,sample2,samplesize):
        # assert len(sample1) < samplesize or len(sample2) < samplesize,'size of samples must be greater than sample size'
        # dir1 = "output/set1"
        # dir2 = "output/set2"
        rsample1 = random.sample(sample1,samplesize)
        rsample2 = random.sample(sample2,samplesize)
        fsample = rsample1 + rsample2
        log.info('size of random sample 1 %s',len(rsample1))
        log.info('size of random sample 2 %s',len(rsample2))
        log.info('calling extraction functions')
        self.extract_to_directory(self.dir1,rsample1)
        self.extract_to_directory(self.dir2,fsample)
    def extract_to_directory(self,destdir,sampleset):
        log.info('removing full path to destination directory if exists')
        if os.path.exists(destdir):
            shutil.rmtree(destdir)
        log.info('starting extraction to destination directory %s',str(destdir))
        if not os.path.exists(destdir):
            log.info('path does not exist so create directory')
            os.makedirs(destdir)
        log.info('Iterate over the sampleset')
        for sample in sampleset:
            full_path = sample.get_filename().rsplit('/',1)
            full_dest_path = os.path.join(destdir,full_path[1])
            if (os.path.isfile(sample.get_filename())):
                shutil.copy(sample.get_filename(),full_dest_path)

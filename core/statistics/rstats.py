#!/usr/bin/env python
import logging
import rpy2.robjects as robjects
log = logging.getLogger(__name__)
class Rstats(object):
    def __init__(self,trialset):
        log.info('initializing Rstats')
        self.trialset = trialset
        self.startdate = self.trialset[0][0]
        self.dt1 = self.trialset[0][1]
        self.dt2 = self.trialset[0][2]
        self.m1 = self.trialset[0][6]
        self.m2 = self.trialset[0][7]
        self.correlations = [trial[3] for trial in self.trialset]
        self.slopes = [trial[4] for trial in self.trialset]
        self.intercepts = [trial[5] for trial in self.trialset]
        self.correlationsv = robjects.FloatVector(self.correlations)
        self.slopesv = robjects.FloatVector(self.slopes)
        self.interceptv = robjects.FloatVector(self.intercepts)
        
    def calc_average(self):
        log.info('calculating averages')
        mean = robjects.r['mean']
        self.averageslope = mean(self.slopesv)[0]
        self.averageintercept = mean(self.interceptv)[0]
        self.averagecorrelation = mean(self.correlationsv)[0]
        log.info('done calculating averages')
    def calc_deviation(self):
        log.info('calculating standard deviation')
        sd = robjects.r['sd']
        self.sdslope = sd(self.slopesv)[0]
        self.sdintercept = sd(self.interceptv)[0]
        self.sdcorrelation = sd(self.correlationsv)[0]
        log.info('done calculating standard deviation')
    def get_stats(self):
        log.info('getting final stats')
        self.calc_average()
        self.calc_deviation()
        log.info('sending back results startdate %s dt1 %s dt2 %s ave-corr %s ave-slope %s ave-intercept %s sd-correlation %s sd-slope %s sd-intercept %s m1 %s m2 %s',str(self.startdate),str(self.dt1),str(self.dt2),str(self.averagecorrelation),str(self.averageslope),str(self.averageintercept),str(self.sdcorrelation),str(self.sdslope),str(self.sdintercept),str(self.m1),str(self.m2))
        result = (self.startdate,self.dt1,self.dt2,
                  self.averagecorrelation,self.averageslope,
                  self.averageintercept,self.sdcorrelation,
                  self.sdslope,self.sdintercept,self.m1,self.m2)
        return result
        
        
            
                
            
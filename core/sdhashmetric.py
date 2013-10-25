from interfaces.idistancemetric import IDistanceMetric
import sdbf_class
import os
import logging

log = logging.getLogger(__name__)

class SdhashMetric(IDistanceMetric):
    
    def distance(self,a,b):
        log.info('Entering sdhash distance')
        test1 = sdbf_class.sdbf(a.get_file_name(),0)
        log.info('test1 %s',str(test1.name()))
        test2 = sdbf_class.sdbf(b.get_file_name(),0)
        log.info('test2 %s',str(test2.name()))
        score = test1.compare(test2,0)
        log.info('similarity score %s',str(score))
        fscore = score / 100.0
        log.info('fixed similarity score %s',str(fscore))
        log.info('fixed disimilarity score %s',str(1-fscore))
        return 1-fscore


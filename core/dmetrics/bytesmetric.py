import logging
import math
from interfaces.idistancemetric import IDistanceMetric
log = logging.getLogger(__name__)

class BytesMetric(IDistanceMetric):
	
	def distance(self,fp1,fp2):
		m1 = fp1.get_malware()
		m2 = fp2.get_malware()
		result = (m1.get_size() - m2.get_size()) 
		return math.fabs(result)

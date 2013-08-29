from interfaces.idistancemetric import IDistanceMetric
import zlib
import logging

log = logging.getLogger(__name__)
class NCDMetric(IDistanceMetric):
	"""NCDMetric Normalized Compressiong Distance
	http://en.wikipedia.org/wiki/Normalized_Compression_Distance"""
	def distance(self,a,b):
		compress = zlib.compress
		da = open(a.get_malware()).read()
		ca = len(compress(da))
		db = open(b.get_malware()).read()
		cb = len(compress(db))
		return ((float(len(compress(da+db)))-min(ca,db))/max(ca,cb))

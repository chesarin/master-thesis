from interfaces.idistancemetric import IDistanceMetric
import zlib
import logging

log = logging.getLogger(__name__)
class NCDMetric(IDistanceMetric):
    """NCDMetric Normalized Compressiong Distance
    http://en.wikipedia.org/wiki/Normalized_Compression_Distance"""
    def distance(self,a,b):
        compress = zlib.compress
        da = open(a.get_file_name(),'rb').read()
        ca = len(compress(da,1))
        db = open(b.get_file_name(),'rb').read()
        cb = len(compress(db,1))
        dab = len(da+db)
        cab = len(compress(da+db))
        log.info('filea %s fileb %s dataA %s dataB %s dAB %s cA %s cB %s cAB %s',
                 str(a),
                 str(b),
                 str(len(da)),
                 str(len(db)),
                 str(dab),
                 str(ca),
                 str(cb),
                 str(cab))
        distance = 1-round(((float(cab)-min(ca,cb))/max(ca,cb)),6)
        log.info('Distance %s',str(distance))
        assert distance >= 0, 'distance must be positive'
        return distance

from core.interfaces.idistancemetric import IDistanceMetric
import logging
import zlib

log = logging.getLogger(__name__)
class ZipMetric(IDistanceMetric):

    def distance(self,a,b):
        compress = zlib.compress
        da = open(a.get_file_name(),'rb').read()
        ca = len(compress(da,1))
        db = open(b.get_file_name(),'rb').read()
        cb = len(compress(db,1))
        dab = len(da+db)
        cab = len(compress(da+db))
        log.info('a %s b %s da %s db %s dab %s ca %s cb %s cab %s',
                 str(a),
                 str(b),
                 str(len(da)),
                 str(len(db)),
                 str(dab),
                 str(ca),
                 str(cb),
                 str(cab))
        distance = round(1-(float(cab) / (ca+cb)),7)
        log.info('Distance %s',str(distance))
        assert distance >= 0.0,'distance must be positive'
        return distance

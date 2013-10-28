from interfaces.idistancemetric import IDistanceMetric
import logging
import zlib

log = logging.getLogger(__name__)
class ZipMetric(IDistanceMetric):

    def distance(self,a,b):
        compress = zlib.compress
        da = open(a.get_file_name()).read()
        ca = len(compress(da))
        db = open(b.get_file_name()).read()
        cb = len(compress(db))
        cc = len(compress(da+db))
        log.info('a %s b %s da %s db %s ca %s cb %s cc %s',
                 str(a),
                 str(b),
                 str(len(da)),
                 str(len(db)),
                 str(ca),
                 str(cb),
                 str(cc))
        distance = float(cc) / (ca+cb)
        log.info('Distance %s',str(distance))
        return 1-distance

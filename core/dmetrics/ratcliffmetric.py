from interfaces.idistancemetric import IDistanceMetric
import difflib
import logging

log = logging.getLogger(__name__)
class RatcliffMetric(IDistanceMetric):
    """
    http://xlinux.nist.gov/dads/HTML/ratcliffObershelp.html
    http://docs.python.org/2/library/difflib.html#difflib.SequenceMatcher
    http://www.drdobbs.com/database/pattern-matching-the-gestalt-approach/184407970?pgno=5
    """
    def distance(self,a,b):
        seq = difflib.SequenceMatcher(a=a.get_xml().lower(),
                                      b=b.get_xml().lower())
        return (1-seq.ratio())

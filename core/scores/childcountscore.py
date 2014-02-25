import logging
import sys
from score.interfaces.iscorer import IScorer

log = logging.getLogger(__name__)

class ChildCountScore(IScorer):

    def computeScore(self,IMalware,IPhylogeny):
        log.info('Computing score based on Child Count')
        malgraph = IPhylogeny.get_graph()
        result = len(malgraph.neighbors(IMalware))
        log.info('malware %s and score %s',str(IMalware),str(result))
        return result
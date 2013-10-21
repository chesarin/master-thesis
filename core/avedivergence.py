#!/usr/bin/env python
import os
import logging
from interfaces.idivcalc import IDivCalc

log = logging.getLogger(__name__)

class AveDivergence(IDivCalc):

    def calcDiv(self,IPred1,IPred2):
        log.info('calculating divergence')
        log.info('total size of keys %s',str(len(IPred1.getKeys())))
        s = 0
        for k in IPred1.getKeys():
            x = IPred1.getPerc(k)
            y = IPred2.getPerc(k)
            log.info('x %s y %s',str(x),str(y))
            s += abs(x - y) / y
            log.info('s %s',str(s))
        result = s / len(IPred1.getKeys())
        log.info('result %s',str(result))
        return result

#!/usr/bin/env python
import os
import logging
from interfaces.idivcalc import IDivCalc

log = logging.getLogger(__name__)

class MaxDivergence(IDivCalc):

    def calcDiv(self,IPred1,IPred2):
        log.info('Calculating MaxDivergence')
        s = 0
        for k in IPred1.getKeys():
            x = IPred1.getPerc(k)
            y = IPred2.getPerc(k)
            log.info('x %s y %s diver %s',str(x),str(y),str(abs(x-y)/y))
            if abs(x-y)/y > s:
                s = abs(x-y)/y
        log.info('max divergence %s',str(s))
        return s

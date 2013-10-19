#!/usr/bin/env python
import os
import logging
from interfaces.idivcalc import IDivCalc

log = logging.getLogger(__name__)

class AveDivergence(IDivCalc):

    def calcDiv(IPred1,IPred2):
        s = 0
        for k in IPred1.get_keys():
            x = IPred1.getPerc(k)
            y = IPred2.getPerc(k)
            s += x - y
        return s /len(IPred1.get_keys())
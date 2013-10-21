#!/usr/bin/env python
from interfaces.ifingerprint import IFingerPrint
class LosslessFingerPrint(IFingerPrint):
    
    def __init__(self,imalware):
        self.malware = imalware
        
    def get_file_name(self):
        """Get malware filename"""
        return self.malware.get_filename()
        
    def get_malware(self):
        """Get malware object"""
        return self.malware

    def __str__(self):
        return '%s' %str(self.malware)
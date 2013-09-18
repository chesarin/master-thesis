#!/usr/bin/env python
from interfaces.ifingerprint import IFingerPrint
class AndroidManifestFingerPrint(IFingerPrint):

    def __init__(self,imalware):
        self.malware = imalware

    def get_file_name(self):
        """Get malware filename"""
        return self.malware.get_filename()

    def get_xml(self):
        return self.malware.get_manifest_xml()
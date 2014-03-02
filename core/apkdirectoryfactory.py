#!/usr/bin/env python
import os
import logging
from interfaces.imalwarecorpusfactory import IMalwareCorpusFactory
from core.malwarecorpus.ramresidentmc import RamResidentMC
from apkmalware import APKFile
# from apkmalware import ApkMalware
log = logging.getLogger(__name__)

class APKDirectoryFactory(IMalwareCorpusFactory):

    def __init__(self):
        self.ramcorpus = RamResidentMC()
        self.validapk = 0
        self.nonvalidapk = 0

    def create(self,directory):
        listing = os.listdir(directory)
        for file in listing:
            temp = directory+"/"+file
            log.info("File name "+temp)
            self.process_apk_file(temp)

    def process_apk_file(self,file):
        log.info("inside process apk files")
        try:
            log.info("Creating APK object")
            # apk = ApkMalware(file)
            apk = APKFile(file)
            log.info("Adding APK object to ramcorpus")
            self.ramcorpus.add(apk)
            log.info("incrementing counter for validapk")
            self.validapk += 1
        except:
            log.info("Exception why")
            self.nonvalidapk += 1

    def get_corpus(self):
        return self.ramcorpus
        

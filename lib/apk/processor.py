import logging
import os
import zipfile
from datetime import datetime

log = logging.getLogger(__name__)

class APKFile(object):
    def __init__(self,filename):
        self.filename = filename
        self.zip = zipfile.ZipFile(filename,'r')
        self.date = self.zip.getinfo('AndroidManifest.xml').date_time
        self.zip.close()
    def get_filename(self):
        return self.filename
    def get_date(self):
        return datetime(*self.date[0:6])
    def __str__(self):
        return '%s %s' %(str(self.filename.rsplit('/')[-1]), str(self.date))

class APKDb(object):
    def __init__(self):
        log.info('Creating APKdb')
        self.db = []
    def add(self,apkfile):
        self.db.append(apkfile)
    def sort_db(self):
        self.db.sort(key=lambda apkfile:apkfile.get_date())
    def __iter__(self):
        return iter(self.db)
    def get_size(self):
        self.sort_db()
        return len(self.db)
    def get_based_date(self):
        return self.db[0].get_date()
    def get_last_item(self):
        return self.db[-1]
        
class APKDirectoryFactory(object):
    def __init__(self,directory):
        self.apkcorpus = APKDb()
        self.create(directory)
    # def set_corpus(self,corpus):
    #     self.apkcorpus = corpus
    def create(self,directory):
        listing = os.listdir(directory)
        for file in listing:
            temp = directory+"/"+file
            self.process_apk_file(temp)
    def process_apk_file(self,file):
        try:
            log.info('starting apk object creation %s',file)
            apk = APKFile(file)
            log.info('Created apk object and adding to corpus')
            log.info('date %s',str(apk.get_date()))
            self.apkcorpus.add(apk)
        except Exception, e :
            log.info('exception %s',file)
            log.exception(e) 
    def get_size(self):
        return self.apkcorpus.get_size()
    def get_corpus(self):
        return self.apkcorpus
    def get_stats(self):
        self.apkcorpus.get_stats()


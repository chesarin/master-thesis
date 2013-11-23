#!/usr/bin/env python
import zipfile
import os
import shutil
import logging
import argparse
import random
import shutil
from time import mktime
from datetime import datetime
from dateutil.relativedelta import relativedelta
log = logging.getLogger(__name__)

class Sampler(object):
    def __init__(self,winsize=1,samplesize=20,startdate=datetime.today()):
        log.info('initializing sampler')
        self.winsize = winsize
        self.samplesize = samplesize
        self.startdate = startdate
        log.info('done initializing')
        
    def setDb(self,db):
        log.info('setting db')
        self.db = db
        log.info('done setting db')
        
    def extract(self):
        log.info('starting extract process')
        log.info('startdate %s',str(self.startdate))
        log.info('window size is %s',str(self.winsize))
        # log.info('type of %s',dir(self.startdate))
        completion = self.db.get_last_item().get_date()
        log.info('completion %s',str(completion))
        while self.startdate < completion: 
            log.info('startdate %s',str(self.startdate))
            samplex = []
            sampley = []
            datetw = self.startdate + relativedelta(months=+self.winsize)
            datetw2 = self.startdate + relativedelta(months=+(2*self.winsize))
            log.info('datetw %s datetw2 %s',str(datetw),str(datetw2))
            for malware in self.db:
                mdate = malware.get_date()
                if mdate >= self.startdate and mdate < datetw:
                    samplex.append(malware)
                    
            for malware in self.db:
                mdate = malware.get_date()
                if mdate >= datetw and mdate < datetw2:
                    sampley.append(malware)
                
            log.info('samplex size %s',len(samplex))
            log.info('sampley size %s',len(sampley))
            self.startdate += relativedelta(months=self.winsize)
            if len(samplex) != 0 and len(sampley) != 0:
                log.info('sets are not zero, we can move on create two directories and called big program')
                log.info('size of samplex %s',len(samplex))
                log.info('size of sampley %s',len(sampley))
                log.info('size of samplesize %s',self.samplesize)
                try:
                    self.create_directories(samplex,sampley,self.samplesize)
                except Exception as e:
                    log.info('Error creating sample directories')
                    log.info('Reason: %s',str(e))
            log.info('startdate %s',str(self.startdate))
    def create_directories(self,sample1,sample2,samplesize):
        # assert len(sample1) < samplesize or len(sample2) < samplesize,'size of samples must be greater than sample size'
        dir1 = "output/set1"
        dir2 = "output/set2"
        rsample1 = random.sample(sample1,samplesize)
        rsample2 = random.sample(sample2,samplesize)
        fsample = rsample1 + rsample2
        log.info('size of random sample 1 %s',len(rsample1))
        log.info('size of random sample 2 %s',len(rsample2))
        log.info('calling extraction functions')
        self.extract_to_directory(dir1,rsample1)
        self.extract_to_directory(dir2,fsample)
    def extract_to_directory(self,destdir,sampleset):
        log.info('starting extraction to destination directory %s',str(destdir))
        if not os.path.exists(destdir):
            log.info('path does not exist so create directory')
            os.makedirs(destdir)
        # shutil.rmtree(destdir)
        log.info('Iterate over the sampleset')
        for sample in sampleset:
            full_path = sample.get_filename().rsplit('/',1)
            full_dest_path = os.path.join(destdir,full_path[1])
            if (os.path.isfile(sample.get_filename())):
                shutil.copy(sample.get_filename(),full_dest_path)
                
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

class APKCorpus(object):
    def __init__(self):
        self.corpus = []

    def add(self,apkfile):
        self.corpus.append(apkfile)

    def get_size(self):
        return len(self.corpus)

    def sort(self):
        self.corpus.sort(key=lambda apkfile:apkfile.date)

    def get_element(self,number):
        return self.corpus[number]
        
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
        
class APKDbDate(object):
    def __init__(self):
        self.db = {}
        
    def add(self,apkfile):
        year = apkfile.get_date()[0]
        log.info('processing year %s',str(year))
        if year in self.db:
            self.db[year].append(apkfile)
        else:
            self.db[year] = []
            self.db[year].append(apkfile)
        
    def get_size(self):
        return len(self.db)
        
    def get_stats(self):
        log.info('APKdbDate')
        log.info('Size of db %s',len(self.db))
        for key in sorted(self.db.keys()):
            log.info('year %s',str(key))
            log.info('samples size %s',str(len(self.db[key])))
    
    def get_keys(self):
        return sorted(self.db.keys())
        
    def get_samples_on(self,year):
        return self.db[year]
        
class APKDirectoryFactory(object):

    # def __init__(self):
    #     self.apkcorpus
        
    def set_corpus(self,corpus):
        self.apkcorpus = corpus
        
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
        
class APKDirectoryExtractor(object):
    
    def set_corpus(self,apkfactory):
        self.corpus = apkfactory.get_corpus()
        
    def extract_from_early(self,outputdir,count):
        # self.corpus.sort()
        self.extract_to_directory(outputdir,count)
        
    def extract_random(self,outputdir,count):
        for year in self.corpus.get_keys():
            if len(self.corpus.get_samples_on(year)) >= count:
                dir = outputdir+'/'+str(year)
                log.info('output dir for year %s',str(dir))
                if not os.path.exists(dir):
                    os.makedirs(dir)
                self.extract_to_directory_yearly(outputdir,count,year)
                
    def extract_to_directory_yearly(self,outputdir,count,year):
        lrandom = random.sample(xrange(count),count)
        malware = self.corpus.get_samples_on(year)
        for sample in lrandom:
            log.info('sample offset to be extracted %s',str(sample))
            log.info('sample to be extracted from %s',
                     str(malware[sample].get_filename()))
            words =  malware[sample].get_filename().rsplit('/',1)
            name = str(year) + '/' + words[1]
            full_dest_path = os.path.join(outputdir,name)
            log.info('sample to be moved to %s',full_dest_path)
            if (os.path.isfile(malware[sample].get_filename())):
                shutil.copy(malware[sample].get_filename(),full_dest_path)
        
    def extract_to_directory(self,outputdir,count):
        for i in range(count):
            element = self.corpus.get_element(i)
            words = element.get_filename().rsplit('/',1)
            ldate = element.get_date()
            full_dest_file_path = os.path.join(outputdir,words[1])
            log.info('%s %s','inputfilename',words[1])
            log.info('%s ',str(ldate))
            log.info('%s %s','outputfile',full_dest_file_path)
            # log.info('%s %s','outputfile',outputdir+'/'+words[1])
            if (os.path.isfile(element.get_filename())):
                shutil.copy(element.get_filename(),full_dest_file_path)
        
def create_factory(inputdirectory,corpus):
    input = APKDirectoryFactory()
    input.set_corpus(corpus)
    input.create(inputdirectory)
    # input.get_stats()
    return input
    
def init_logging(args):
    if args.quiet:
        logging.basicConfig(filename='application.log',
                            filemode='w',
                            level=logging.WARN,
                            format='%(asctime)s %(name)s %(funcName)s %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    elif args.debug:
        logging.basicConfig(filename='processapk.log',
                            filemode='w',
                            level=logging.DEBUG,
                            format='%(asctime)s %(name)s %(funcName)s %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p')

def init_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q","--quiet",
                        help="Display only error messages",
                        action="store_true",required=False)
    parser.add_argument("-d","--debug",
                        help="Display debug messages",
                        action="store_true",required=False)
    parser.add_argument("-dir","--inputdirectory",
                        help="Directory to read input from",
                        default="data",
                        required=False)
    parser.add_argument("-outdir","--outputdirectory",
                        help="Output directory for results",
                        default="output",
                        required=False)
    parser.add_argument("-nitems","--numberofitems",
                        help="number of items to extract",
                        type=int,
                        default='1',
                        required=False)

    return parser

        
def main():
    """Initiate arguments, logs and dictionary to be used to extract parameters"""
    parser = init_arguments()
    args = parser.parse_args()
    dic_args = vars(args)
    init_logging(args)
    """Actual Works Start Here"""
    log.info('Starts')
    corpus = APKDb()
    factory = create_factory(dic_args['inputdirectory'],corpus)
    log.info('%s %s','size of factory',str(factory.get_size()))
    corpus = factory.get_corpus()
    sdate = corpus.get_based_date()
    log.info('date that will be used as the base %s',str(sdate))
    sampler = Sampler(6,20,sdate)
    sampler.setDb(corpus)
    sampler.extract()
    for i in corpus:
        log.info('file %s',str(i))
    # extractor = APKDirectoryExtractor()
    # extractor.set_corpus(factory)
    # extractor.extract_random(dic_args['outputdirectory'],
    #                              dic_args['numberofitems'])
    log.info('Ends')
    

if __name__== '__main__':
    main()
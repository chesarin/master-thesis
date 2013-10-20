#!/usr/bin/env python
import zipfile
import os
import shutil
import logging
import argparse
import random

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
        # manifest = self.zip.getinfo('AndroidManifest.xml')
        # self.date = manifest.date_time
        return self.date

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
    input.get_stats()
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
    corpus = APKDbDate()
    factory = create_factory(dic_args['inputdirectory'],corpus)
    log.info('%s %s','size of factory',str(factory.get_size()))
    extractor = APKDirectoryExtractor()
    extractor.set_corpus(factory)
    extractor.extract_random(dic_args['outputdirectory'],
                                 dic_args['numberofitems'])
    # extractor.extract_from_early(dic_args['outputdirectory'],
    #                              dic_args['numberofitems'],factory)
    log.info('Ends')
    

if __name__== '__main__':
    main()
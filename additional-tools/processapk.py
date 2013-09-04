#!/usr/bin/env python
import zipfile
import os
import shutil
import logging
import argparse

log = logging.getLogger(__name__)

class APKFile(object):
    def __init__(self,filename):
        self.filename = filename
        self.zip = zipfile.ZipFile(filename,'r')
        self.date = self.zip.getinfo('AndroidManifest.xml')
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

class APKDirectoryFactory(object):

    def __init__(self):
        self.apkcorpus = APKCorpus()

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
            self.apkcorpus.add(apk)
        except Exception, e :
            log.info('exception %s',file)
            log.exception(e) 
            
    def get_size(self):
        return self.apkcorpus.get_size()

    def get_corpus(self):
        return self.apkcorpus
            
class APKDirectoryExtractor(object):
    
    def __init__(self):
        """test"""
        
    def extract_from_early(self,outputdir,count,apkfactory):
        self.corpus = apkfactory.get_corpus()
        self.corpus.sort()
        self.extract_to_directory(outputdir,count)
        
    def extract_to_directory(self,outputdir,count):
        for i in range(count):
            words = self.corpus.get_element(i).get_filename().rsplit('/',1)
            log.info('%s %s','inputfilename',words[1])
            log.info('%s %s','outputfile',outputdir+'/'+words[1])
        
def create_factory(inputdirectory,outputdirectory):
    input = APKDirectoryFactory()
    input.create(inputdirectory)
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
    factory = create_factory(dic_args['inputdirectory'],
                             dic_args['outputdirectory'])
    log.info('%s %s','size of factory',str(factory.get_size()))
    extractor = APKDirectoryExtractor()
    extractor.extract_from_early(dic_args['outputdirectory'],
                                 dic_args['numberofitems'],factory)
    log.info('Ends')
    

if __name__== '__main__':
    main()
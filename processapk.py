#!/usr/bin/env python
import zipfile
import os
import shutil
import logging
import argparse
import random
import time
import csv
import shutil
from time import mktime
from datetime import datetime
from core.statistics.rstats import Rstats
from core.dmetrics.ratcliffmetric import RatcliffMetric
from core.apk.apkdirectoryfactory import APKDirectoryFactory
from core.fingerprints.androidmanifestfingerprintfactory import AndroidManifestFingerPrintFactory
from dateutil.relativedelta import relativedelta
from lib.apk.processor import APKDbDirectoryFactory
from core.factories.disdbfactory import DisDBFactory
from core.plots.distancehistogram import DistanceHistogram
from core.analysis.analysismodels import ManifestAnalysis
from core.predictions.treepredictor import TreePredictor,LinearRegTreePredictor,LogisticRegTreePredictor,TreePredictorClassifier
from core.apk.apksampleset import ApkSampleSet
from core.interfaces.isampler import RandomSampler, TwoSamplesExtractor
from core.ml.trainer import LinerRegressionTrainer,LogisticRegressionTrainer
from core.phylogeny.phyfeatures import NodeAgeFromRoot,NodeAgeFromLatest,AgeLatestChild,AgeNewestDescendant
# from timeit import timeit
import timeit
log = logging.getLogger(__name__)

class Sampler(object):
    def __init__(self,winsize=1,samplesize=20,startdate=datetime.today(),outdir='output',ntrials=4, features=2):
        log.info('initializing Sampler')
        self.winsize = winsize
        self.samplesize = samplesize
        self.startdate = startdate
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.dir1 = outdir +"/set1-"+ self.timestr
        self.dir2 = outdir + "/set2-"+ self.timestr
        self.outdir = outdir
        self.ntrials = ntrials
        self.features = features
        self.stats = []
        self.trainer_stats = []
        log.info('done initializing')
        
    def setDb(self,db):
        log.info('setting db')
        self.db = db
        log.info('done setting db')
        
    def extract(self):
        startdate = self.startdate
        log.info('starting extract process')
        log.info('startdate %s',str(startdate))
        log.info('window size is %s',str(self.winsize))
        # completion = self.db.get_last_item().get_date()
        completion = self.db.get_last_sample_date()
        log.info('completion %s',str(completion))
        while startdate < completion: 
            log.info('startdate %s',str(startdate))
            sampler = RandomSampler(self.db, self.samplesize, startdate, self.winsize)
            # samplex = []
            # sampley = []
            # datetw = startdate + relativedelta(months=+self.winsize)
            # datetw2 = startdate + relativedelta(months=+(2*self.winsize))
            # log.info('datetw %s datetw2 %s',str(datetw),str(datetw2))
            # for malware in self.db:
            #     mdate = malware.get_date()
            #     if mdate >= startdate and mdate < datetw:
            #         samplex.append(malware)
                    
            # for malware in self.db:
            #     mdate = malware.get_date()
            #     if mdate >= datetw and mdate < datetw2:
            #         sampley.append(malware)
                
            # log.info('samplex size %s',len(samplex))
            # log.info('sampley size %s',len(sampley))
            # if len(samplex) != 0 and len(sampley) != 0:
            if sampler.enough_data():
                log.info('sets are not zero, we can move on create two directories and called big program')
                presentsample, futuresample = sampler.get_samples()
                extractor = TwoSamplesExtractor(presentsample, futuresample, self.outdir)
                extractor.extract_samples_sets()
                analysisobject = ManifestAnalysis()
                path1, path2 = extractor.get_paths()
                # predictor = TreePredictorClassifier(analysisobject, path1, path2, outputdir)
                predictor = TreePredictor(analysisobject, path1, path2, self.outdir)
                predictor.create_perfect_prediction()
                predictor.create_estimated_prediction()
                predictor.create_predictions_db()
                predictor.compute_stats()
                predictor.set_visuallizer()
                predictor.plot_predictions()
                predictor.create_visuallization()
                predictor.create_predictions_db_file()
                trainer = LinerRegressionTrainer(predictor, presentsample, self.features)
                # trainer = LogisticRegressionTrainer(predictor, presentsample, num_of_features)
                trainer.create_training_set()
                trainer.calculate_thetas()
                trainer.create_trainingset_file(self.outdir)
                trainer.create_xy_file(self.outdir)
                trainer.create_phylogeny_file(self.outdir)
                thetas = trainer.get_thetas()
                self.trainer_stats.append([startdate.date(),completion.date(),sampler.get_full_sample_size()]+thetas)
                # log.info('size of samplex %s',len(samplex))
                # log.info('size of sampley %s',len(sampley))
                # log.info('size of samplesize %s',self.samplesize)
                try:
                # self.trials(samplex,sampley,startdate,datetw,datetw2)
                    datetw = startdate
                    datetw2 = startdate + relativedelta(months=+(2*self.winsize))
                    self.trials(self.db, startdate, datetw, datetw2, thetas)
                    # self.create_directories(samplex,sampley,self.samplesize)
                    # log.info('done creating directories')
                    # log.info('creating dfactory')
                    # dfactory = APKDirectoryFactory()
                    # log.info('creating fingerprintfactory')
                    # fpf = AndroidManifestFingerPrintFactory()
                    # log.info('creating metric')
                    # dis = RatcliffMetric()
                    # log.info('initializing predictorfactory')
                    # predictorfactory = PredictorFactory(self.dir1,self.dir2,self.outdir)
                    # predictorfactory.set_factories(dfactory,fpf,dis)
                    # predictorfactory.execute()
                except Exception as e:
                    log.info('Error creating sample directories')
                    log.info('Reason: %s',str(e))
            # log.info('startdate %s',str(startdate))
            startdate += relativedelta(months=self.winsize)

    def create_directories(self,sample1,sample2,samplesize):
        rsample1 = random.sample(sample1,samplesize)
        rsample2 = random.sample(sample2,samplesize)
        fsample = rsample1 + rsample2
        log.info('size of random sample 1 %s',len(rsample1))
        log.info('size of random sample 2 %s',len(rsample2))
        log.info('calling extraction functions')
        self.extract_to_directory(self.dir1,rsample1)
        self.extract_to_directory(self.dir2,fsample)
    def extract_to_directory(self,destdir,sampleset):
        log.info('removing full path to destination directory if exists')
        if os.path.exists(destdir):
            shutil.rmtree(destdir)
        log.info('starting extraction to destination directory %s',str(destdir))
        if not os.path.exists(destdir):
            log.info('path does not exist so create directory')
            os.makedirs(destdir)
        log.info('Iterate over the sampleset')
        for sample in sampleset:
            full_path = sample.get_filename().rsplit('/',1)
            full_dest_path = os.path.join(destdir,full_path[1])
            if (os.path.isfile(sample.get_filename())):
                shutil.copy(sample.get_filename(),full_dest_path)

    # def trials(self,samplex,sampley,startdate,datetw,datetw2):
    def trials(self, sampleset, startdate, datetw, datetw2, thetas):
        statslist = []
        for trial in range(self.ntrials):
            sampler = RandomSampler(sampleset, self.samplesize, startdate, self.winsize)
            if sampler.enough_data():
                presentsample, futuresample = sampler.get_samples()
                self.create_directories(presentsample, futuresample, self.samplesize)
                log.info('trial function and trial number is %s',str(trial))
                log.info('startdate:%s ',str(startdate))
                log.info('done creating directories')
                analysisobject = ManifestAnalysis()
                # predictor = TreePredictor(analysisobject,self.dir1,self.dir2,self.outdir)
                predictor = LinearRegTreePredictor(analysisobject,self.dir1, self.dir2, self.outdir)
                predictor.create_perfect_prediction()
                predictor.create_estimated_prediction(thetas, self.features)
                # predictor.create_estimated_prediction()
                predictor.create_predictions_db()
                predictor.compute_stats()
                predictor.set_visuallizer()
                predictor.plot_predictions()
                predictor.create_visuallization()
                predictor.create_predictions_db_file()
                r,m,b = predictor.get_statistics()
                result = startdate.date(),datetw.date(),datetw2.date(),r,m,b,len(presentsample),len(futuresample)
                statslist.append(result)
        log.info('done executing 4 trials')
        tr2 = 0
        rstats = Rstats(statslist)
        groupstats = rstats.get_stats()
        statslist.append(groupstats)
        log.info('trying to iterate over statslist')
        for stat in statslist:
            if len(stat) == 8:
                sd,dt1,dt2,r,m,b,m1,m2 = stat
                log.info('startdate:%s datetw:%s datetw2:%s trial num:%s correlation:%s slope:%s y-intercept:%s m1:%s m2:%s',
                     str(sd),str(dt1),str(dt2),str(tr2),str(r),str(m),str(b),str(m1),str(m2))
            else:
                sd,dt1,dt2,r,m,b,sr,sm,sb,m1,m2 = stat
                log.info('startdate:%s datetw:%s datetw2:%s trial num:%s ave-correlation:%s ave-slope:%s ave-intercept:%s st-correlation:%s st-slope:%s st-intercept %s m1:%s m2:%s',
                         str(sd),str(dt1),str(dt2),str(tr2),str(r),str(m),str(b),str(sr),str(sm),str(sb),str(m1),str(m2))

            tr2 += 1
        self.stats.append(statslist)
    def get_stats(self):
        return self.stats
    def create_file(self):
        directory = self.outdir + '/stats/'
        if not os.path.exists(directory):
            log.info('path does not exist so create directory')
            os.makedirs(directory)
        paramheader = "window-size(months)={:3} samplesize(malware samples)={:3} initial-sample-date(earliest-sample)={:10} num-of-trials={:3}\n".format(str(self.winsize),str(self.samplesize),str(self.startdate.date()),str(self.ntrials))
        header1 = "{:10}\t{:10}\t{:10}\t{:4}\t{:4}\t{:4}\t{:4}\t{:4}\n".format('sdate','date1','date2','r','m','b','m1','m2')
        header2 = "{:10}\t{:10}\t{:10}\t{:4}\t{:4}\t{:4}\t{:4}\t{:4}\t{:4}\t{:4}\t{:4}\n".format('sdate','date1','date2','ar','am','ab','sdr','sdm','sdb','m1','m2')
        trainerfile = directory + 'trainer.csv'
        trainer_header = ['StartDate', 'Completion Date','size of sampler', 'thetas']
        with open(trainerfile, 'w') as tfile:
            f_csv = csv.writer(tfile)
            f_csv.writerow(trainer_header)
            f_csv.writerows(self.trainer_stats)
        trialsfile = directory + 'trials.csv'
        averagesfile = directory + 'averages.csv'
        trials = [trial for trialset in self.stats for trial in trialset if len(trial) == 8]
        averages = [trial for trialset in self.stats for trial in trialset if len(trial) > 8]
        with open(trialsfile,'wb') as fp1:
            fp1.write(paramheader)
            fp1.write(header1)
            for t in trials:
                sd,dt1,dt2,r,m,b,m1,m2 = t
                value = "{:10}\t{:10}\t{:10}\t{:4}\t{:4}\t{:4}\t{:4}\t{:4}\n".format(str(sd),str(dt1),str(dt2),str(round(r,4)),str(round(m,4)),str(round(b,4)),str(m1),str(m2))
                fp1.write(value)
        with open(averagesfile,'wb') as fp2:
            fp2.write(paramheader)
            fp2.write(header2)
            for t in averages:
                sd,dt1,dt2,r,m,b,sr,sm,sb,m1,m2 = t
                value = "{:10}\t{:10}\t{:10}\t{:4}\t{:4}\t{:4}\t{:4}\t{:4}\t{:4}\t{:4}\t{:4}\n".format(str(sd),str(dt1),str(dt2),
                                                                                                       str(round(r,4)),str(round(m,4)),str(round(b,4)),
                                                                                                       str(round(sr,4)),str(round(sm,4)),str(round(sb,4)),
                                                                                                       str(m1),str(m2))
                fp2.write(value)

                
                
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
        
# def create_factory(inputdirectory,corpus):
#     input = APKDirectoryFactory()
#     input.set_corpus(corpus)
#     input.create(inputdirectory)
#     # input.get_stats()
#     return input
    
def init_logging(args):
    timestr = time.strftime("%Y%m%d-%H%M")
    lfile = 'processapk' + timestr + '.log'
    if args.quiet:
        logging.basicConfig(filename=lfile,
                            filemode='w',
                            level=logging.WARN,
                            format='%(asctime)s %(name)s %(funcName)s %(message)s', 
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    elif args.debug:
        logging.basicConfig(filename=lfile,
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
                        required=True)
    parser.add_argument("-outdir","--outputdirectory",
                        help="Output directory for results",
                        default="output",
                        required=False)
    parser.add_argument("-nitems","--numberofitems",
                        help="number of items per sample default is 20",
                        type=int,
                        default='20',
                        required=False)
    parser.add_argument("-window","--windowsize",
                        help="window size in months default is 2 months",
                        type=int,
                        default='2',
                        required=False)
    parser.add_argument("-trials","--ntrials",
                        help="number of trials default is 4",
                        type=int,
                        default='4',
                        required=False)
    parser.add_argument("-features","--nfeatures",
                        help="number of feature use for machine learning defaults to 2",
                        type=int,
                        default='2',
                        required=False)

    return parser
def controlSampler(inputDir,windowSize,nitems,outputDir,trials, features):
    # factory = APKDbDirectoryFactory(inputDir)
    # log.info('%s %s','size of factory',str(factory.get_size()))
    # corpus = factory.get_corpus()
    features = features
    corpus = ApkSampleSet(inputDir)
    # sdate = corpus.get_based_date()
    sdate = corpus.get_first_sample_date()
    log.info('date that will be used as the base %s',str(sdate))
    sampler = Sampler(windowSize,nitems,sdate,outputDir,trials, features)
    sampler.setDb(corpus)
    sampler.extract()
    sampler.create_file()
        
def control_distance_histogram(indir,outdir):
    dfactory = APKDirectoryFactory()
    fpf = AndroidManifestFingerPrintFactory()
    dis = RatcliffMetric()
    disdbfactory = DisDBFactory(indir,dis,fpf,dfactory)
    disdb = disdbfactory.create()
    histogramfactory = DistanceHistogram(disdb)
    histogram = histogramfactory.create()
    histogram.plot_pdf(outdir)

def control_trainer(indir, nitems, windowsize, outputdir, num_of_features):
    sampleset = ApkSampleSet(indir)
    # date1 = datetime(2011, 03, 01)
    firstsampledate = sampleset.get_first_sample_date()
    lastsampledate = sampleset.get_last_sample_date()
    while firstsampledate <= lastsampledate:
        sampler = RandomSampler(sampleset, nitems, firstsampledate, windowsize)
        if sampler.enough_data():
            presentsample, futuresample = sampler.get_samples()
            extractor = TwoSamplesExtractor(presentsample, futuresample, outputdir)
            extractor.extract_samples_sets()
            analysisobject = ManifestAnalysis()
            path1, path2 = extractor.get_paths()
            # predictor = TreePredictorClassifier(analysisobject, path1, path2, outputdir)
            predictor = TreePredictor(analysisobject, path1, path2, outputdir)
            predictor.create_perfect_prediction()
            predictor.create_estimated_prediction()
            predictor.create_predictions_db()
            predictor.compute_stats()
            predictor.set_visuallizer()
            predictor.plot_predictions()
            predictor.create_visuallization()
            predictor.create_predictions_db_file()
            trainer = LinerRegressionTrainer(predictor, presentsample, num_of_features)
            # trainer = LogisticRegressionTrainer(predictor, presentsample, num_of_features)
            trainer.create_training_set()
            trainer.calculate_thetas()
            trainer.create_trainingset_file(outputdir)
            trainer.create_xy_file(outputdir)
            trainer.create_phylogeny_file(outputdir)
            thetas = trainer.get_thetas()
            analysisobject2 = ManifestAnalysis()
            predictor2 = LinearRegTreePredictor(analysisobject2, path1, path2, outputdir)
            # predictor2 = LogisticRegTreePredictor(analysisobject2, path1, path2, outputdir)
            predictor2.create_perfect_prediction()
            predictor2.create_estimated_prediction(thetas, num_of_features)
            predictor2.create_predictions_db()
            predictor2.compute_stats()
            predictor2.set_visuallizer()
            predictor2.plot_predictions()
            predictor2.create_visuallization()
            predictor2.create_predictions_db_file()
            break
        else:
            # print 'not enough malware to use incrementing firstsampledate'
            firstsampledate += relativedelta(months=windowsize)
def test_phylogeny_features(dir1, dir2, outputdir):
    from core.apk.apkdirectoryfactory import APKDirectoryFactory
    analysisobject = ManifestAnalysis()
    predictor = TreePredictor(analysisobject, dir1, dir2, outputdir)
    phylogeny1 = predictor.get_phylogeny1()
    dirfactory = APKDirectoryFactory()
    graph = phylogeny1.get_graph()
    dirfactory.create(dir1)
    mc = dirfactory.get_corpus()
    corpus = mc.get_mc_corpus()
    print 'iterating over corpus'
    for i in corpus:
        # feature = AgeFromParent(graph, i)
        # feature = ChildrenNumber(graph, i)
        # feature = DistanceFromParent(graph, i)
        # feature = NodeAgeFromRoot(graph, i)
        feature = NodeAgeFromLatest(graph, i)
        # feature = AgeLatestChild(graph, i)
        # feature = AgeNewestDescendant(graph, i)
        feature.compute_feature()
        name = feature.get_name()
        value = feature.get_value()
        print 'malware {0} feature-name {1} feature-value {2}'.format(i, name, value)
    # print graph
    
def main():
    """Initiate arguments, logs and dictionary to be used to extract parameters"""
    parser = init_arguments()
    args = parser.parse_args()
    init_logging(args)
    """Actual Works Start Here"""
    log.info('Starts')
    # dir1 = 'malware/20-set'
    # dir2 = 'malware/40-set'
    # test_phylogeny_features(dir1, dir2, args.outputdirectory)
    # control_trainer(args.inputdirectory, args.numberofitems, args.windowsize, args.outputdirectory, args.nfeatures)
    controlSampler(args.inputdirectory, args.windowsize,
                   args.numberofitems,args.outputdirectory,
                   args.ntrials, args.nfeatures)
    # control_distance_histogram(args.inputdirectory, args.outputdirectory)
    # textract = timeit.Timer(sampler.extract).timeit(1)
    # log.info('time it took to extract from sampler %s',str(textract))
    log.info('Ends')
    

if __name__== '__main__':
    main()
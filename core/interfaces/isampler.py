from zope.interface import Interface
from dateutil.relativedelta import relativedelta
import random
import time
import os
import shutil
class Isampler(Interface):
    """Interface to choose random sample set of malware"""
    def __init__(malwarecorpus,windowsize,trialsize,trials):
        """
        Isampler constructor takes the following:
        malwareset:malware set to choose from
        windowsize:integer value of months in between samples
        trialsize:integer value for the number of malware samples to choose
        for each windowsize
        trials:number of trials for each windowsize
        """
    def _chooseSampleTrial(sampleset,trialsize,trialnum):
        """
        _chooseSampleTrial: Function to extract random samples from malwareset
        start=date variable from where the sample should be chosen from
        end=date variable used to limit the maximum date that we can choose from
        samplesize=the sample size that we should extract from malwareset
        trialnum=the trial number
        """
    def _chooseSampleSets(start,end,windowsize):
        """
        _chooseSampleSets: Function to extract a sample set based the following parameters
        start=date of first malware found on the malwarecorpus
        end=date of last malware found on the malwarecorpus
        windowsize=window size based on months for each malware set that must be chosen
        """
    def _extractStats(sampletrial):
        """
        _extractStats: Function to extract statistics based from the sampletrial
        The basic stats we need are
        R:Correlation Coefficient
        M:Slope
        B:Y-intercept
        """
class RandomSampler(object):
    def __init__(self, sampleset, size, sdate, windowsize):
        self.sampleset = sampleset
        self.samplesize = size
        self.startdate = sdate
        self.windowsize = windowsize
        self.presentsampleset = []
        self.futuresampleset = []
    def _create_random_sample(self, startdate):
        fullsample = self.sampleset.create_sample_subset(startdate, self.windowsize)
        if len(fullsample) > self.samplesize:
            randomsample = random.sample(fullsample, self.samplesize)
        else:
            randomsample = []
        return randomsample
    def _create_samples(self):
        presentdate = self.startdate
        presentsampleset = self._create_random_sample(presentdate)
        futuredate = self.startdate + relativedelta(months=+self.windowsize)
        futuresampleset = self._create_random_sample(futuredate)
        return (presentsampleset, futuresampleset)
    def enough_data(self):
        value = False
        sample1, sample2 = self._create_samples()
        threshold = self.samplesize
        if len(sample1) == threshold and len(sample2) == threshold:
            self.presentsampleset = sample1
            self.futuresampleset = sample2
            value = True
        return value
    def get_samples(self):
        return self.presentsampleset, self.futuresampleset

        
class SampleSet(object):
    """Sampler class used to create a list of files for a specific date range
    nsamples=the number of samples
    windowsize=the number of months for the completion date of the range
    startdate=a date to use to start picking samples
    filesdb=the files stored in memory to choose samples from
    they should be sorted"""
    def __init__(self, ramresidentmc):
        self.sampleslist = ramresidentmc.get_mc_corpus()
    def create_sample_subset(self, sdate, windowsize=4):
        samplelist = []
        startdate = sdate
        completiondate = startdate + relativedelta(months=+windowsize)
        for f in self.sampleslist:
            fdate = f.get_date()
            if fdate >= startdate and fdate < completiondate:
                samplelist.append(f)
        return samplelist
    def get_first_sample_date(self):
        return self.sampleslist[0].get_date()
    def get_last_sample_date(self):
        return self.sampleslist[-1].get_date()
class TwoSamplesExtractor(object):
    def __init__(self, sample1, sample2, outputdir='/tmp/output/malware-sets'):
        self.sample1 = sample1
        self.sample2 = sample2
        self.outputdir = outputdir
        self.sample1fullpath = ''
        self.sample2fullpath = ''
        self.timestr = time.strftime("%Y%m%d-%H%M")

    def _create_directory(self, setname, destdir):
        directory = destdir + "/" + setname + self.timestr
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory
    def _clean_up(self, destdir):
        if os.path.exists(destdir):
            shutil.rmtree(destdir)
        
    def _extract_sample(self, sampleset, destdir):
        for sample in sampleset:
            full_path = sample.get_filename().rsplit('/',1)
            full_dest_path = os.path.join(destdir,full_path[1])
            if (os.path.isfile(sample.get_filename())):
                shutil.copy(sample.get_filename(),full_dest_path)

    def extract_samples_sets(self):
        destdir = self.outputdir + '/ml-training-sets'
        self._clean_up(destdir)
        initialsample = self.sample1
        finalsample = self.sample1 + self.sample2
        # print 'size of initialsample {}'.format(len(initialsample))
        # print 'size of finalsample {}'.format(len(finalsample))
        dir1 = self._create_directory('set1-', destdir)
        self._extract_sample(initialsample, dir1)
        self.sample1fullpath = dir1
        dir2 = self._create_directory('set2-', destdir)
        self._extract_sample(finalsample, dir2)
        self.sample2fullpath = dir2
        
    def get_paths(self):
        return self.sample1fullpath, self.sample2fullpath
        
    
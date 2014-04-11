from core.interfaces.ifeature import NumericFeature
from androguard.core.bytecodes import dvm
import logging
LOG = logging.getLogger(__name__)
class DangerousPermissions(NumericFeature):
    def __init__(self, ApkFile):
        LOG.info('initializing')
        NumericFeature.__init__(self,ApkFile.get_apk(),'DangerousPermissions')
        LOG.info('done initializing %s',self.name)
    def compute_feature(self):
        try:
            permdic = self.malware.get_details_permissions()
            permlist = [key for key,value in permdic.iteritems() if value[0] == 'dangerous']
            self.value = len(permlist)
        except Exception as e:
            LOG.info('Not able to create Dangerous Permissions Feature')
            LOG.info('Reason %s', str(e))
            
class NumberReceivers(NumericFeature):
    def __init__(self, ApkFile):
        LOG.info('initializing')
        NumericFeature.__init__(self,ApkFile.get_apk(),'NumberReceivers')
        LOG.info('done initializing %s', self.name)
    def compute_feature(self):
        try:
            receiverslist = self.malware.get_receivers()
            self.value = len(receiverslist)
        except Exception as e:
            LOG.info('Not able to create number of receivers feaure')
            LOG.info('Reason %s',str(e))
class NumberDexClasses(NumericFeature):
    def __init__(self,ApkFile):
        LOG.info('initializing')
        apk = ApkFile.get_apk()
        dexfile = dvm.DalvikVMFormat(apk.get_dex())
        NumericFeature.__init__(self,dexfile,'NumberDexClasses')
        LOG.info('done initializing %s',self.name)
    def compute_feature(self):
        try:
            classeslist = self.malware.get_classes()
            self.value = len(classeslist)
        except Exception as e:
            LOG.info('Not able to create Number of Dex Classes')
            LOG.info('Reason %s', str(e))
        

import logging
from disdb import DisDB

log = logging.getLogger(__name__)


class DisDBFactory(object):
    def __init__(self,inputdir,metric,fpfactory,outputfile):
        self.db = DisDB(inputdir,metric,fpfactory,outputfile)
    def create_output_file(self):
        self.db.create_file()
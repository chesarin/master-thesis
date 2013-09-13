import logging
import json

log = logging.getLogger(__name__)

class GraphJson(object):
    def __init__(self,Graph):
        self.Graph = Graph.get_graph()
    def create_dict(self,node):
        if not len(self.Graph.successors(node)):
            return {
                'id':str(node),
                'name':str(node)[:7]
            }
        return {
            'id':str(node),
            'name':str(node)[:7],
            'children':map(self.create_dict,self.Graph.successors(node))
        }
    def create_json_file(self,filename):
        root = self.Graph.get_root()
        log.info('print root %s',str(root))
        data = self.create_dict(root)
        log.info('writing the following to filename: %s',data)
        with open(filename,'wb') as fp:
            json.dump(data,fp,sort_keys=True,indent=1,separators=(',',':'))

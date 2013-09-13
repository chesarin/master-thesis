import logging
import json

log = logging.getLogger(__name__)

class GraphJson(object):
    def __init__(self,Graph):
        log.info('initialing GraphJson')
        self.Graph = Graph.get_graph()
        log.info("let's iterate over the nodes in this graph")
        for node in self.Graph.iternodes():
            log.info('node %s and date %s',
                     str(node),
                     str(node.attr['comment']))
    def create_dict(self,node):
        log.info('node id:%s date:%s',
                 str(node),
                 str(node.attr['comment']))
        if not len(self.Graph.successors(node)):
            return {
                'id':str(node),
                'name':''
                # 'data':{
                #     'date':str(node.attr['comment'])
                # }
            }
        return {
            'id':str(node),
            'name':'',
            # 'data':{
            #     'date':str(node.attr['comment'])
            # },
            'children':map(self.create_dict,
                           self.Graph.successors_iter(node))
        }
    def create_json_file(self,filename):
        log.info('creating json file at %s',filename)
        root = self.Graph.get_root()
        log.info('print root %s',str(root))
        data = self.create_dict(root)
        log.info('writing the following to filename: %s',data)
        with open(filename,'wb') as fp:
            json.dump(data,fp,sort_keys=True,indent=1,separators=(',',':'))

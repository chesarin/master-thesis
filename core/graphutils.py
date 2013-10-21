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
        roots = self.Graph.get_root()
        log.info('print root %s',str(roots))
        log.info('print len of roots %s',str(len(roots)))
        if len(roots) == 1:
            log.info('inside if len of roots is 1')
            data = self.create_dict(roots[0])
        else:
            log.info('inside if there are more than one roots')
            data = self.create_json_for_graph()
        # data = self.create_dict(root)
        log.info('writing the following to filename: %s',data)
        with open(filename,'wb') as fp:
            # json.dump(data,fp,sort_keys=True,indent=1,separators=(',',':'))
            json.dump(data,fp)
    def create_json_for_graph(self):
        nodes = self.Graph.nodes()
        data = []
        for node in nodes:
            data.append({'id':str(node),
                         'name':str(node)[:6],
                         'adjacencies':self.Graph.successors(node)})
        log.info('writting the following to filename: %s',data)
        return data
    def create_edges_file(self,filename):
        log.info('creating text file:%s of edges',filename)
        outputfile=open(filename,'w')
        for nodea,nodeb,distance in self.Graph.edges(keys='True'):
            log.info('%s %s %s',nodea,nodeb,distance)
            outputfile.write('%s %s %s \n' %(nodea,nodeb,distance))
            
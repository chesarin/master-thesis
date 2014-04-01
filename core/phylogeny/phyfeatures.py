from core.interfaces.ifeature import PhylogenyNumericFeature
from core.algorithms.bfs import Bfs
from datetime import datetime
import logging
LOG = logging.getLogger(__name__)
class NodesAge(object):
    def __init__(self, nodea, nodeb):
        self.nodea = nodea
        self.nodeb = nodeb
    def _get_date_attributes(self):
        datea = self.nodea.attr['comment']
        dateb = self.nodeb.attr['comment']
        return datea, dateb
    def get_age(self):
        temp1, temp2 = self._get_date_attributes()
        datea = datetime.strptime(temp1,'%Y-%m-%d %H:%M:%S')
        dateb = datetime.strptime(temp2,'%Y-%m-%d %H:%M:%S')
        diff = dateb - datea
        # LOG.info('diff %', diff)
        LOG.info('days %s', diff.days)
        LOG.info('seconds %s', diff.seconds)
        LOG.info('total seconds %s', diff.total_seconds())
        return diff.total_seconds()
    
        
class ChildrenNumber(PhylogenyNumericFeature):
    def __init__(self, Graph, ApkFile):
        LOG.info('initilizing')
        apk = ApkFile
        graph = Graph
        PhylogenyNumericFeature.__init__(self, graph, apk, 'children-number')
        LOG.info('done initializing %s', self.name)
    def compute_feature(self):
        """
        1. Get the graph from the phylogeny
        2. Get the node that belongs to the current malware from the graph.
        3. Get the number of children from the graph of the node
        object obtained from step 2.
        """
        malware = self.malware
        graph = self.phylogeny
        node = graph.get_node(str(malware))
        children = graph.get_number_of_children(node)
        self.value = children
class AgeFromParent(PhylogenyNumericFeature):
    def __init__(self, Graph, ApkFile):
        LOG.info('initilizing')
        apk = ApkFile
        graph = Graph
        PhylogenyNumericFeature.__init__(self, graph, apk, 'age-from-parent')
        LOG.info('done initializing %s', self.name)
    def compute_feature(self):
        malware = self.malware
        graph = self.phylogeny
        child_node = graph.get_node(str(malware))
        parents = graph.predecessors(child_node)
        if len(parents) == 0:
            age = 0
        else:
            parent_node = parents[0]
            age_extractor = NodesAge(parent_node, child_node)
            age = age_extractor.get_age()
        self.value = age
class DistanceFromParent(PhylogenyNumericFeature):
    def __init__(self, Graph, ApkFile):
        LOG.info('initilizing')
        apk = ApkFile
        graph = Graph
        PhylogenyNumericFeature.__init__(self, graph, apk, 'distance-from-parent')
        LOG.info('done initializing %s', self.name)
    def compute_feature(self):
        malware = self.malware
        graph = self.phylogeny
        child_node = graph.get_node(str(malware))
        parents = graph.predecessors(child_node)
        if len(parents) == 0:
            distance = 0
        else:
            parent_node = parents[0]
            edge = graph.get_edge(parent_node,child_node)
            distance = edge.attr['label']
        self.value = distance
class NodeAgeFromRoot(PhylogenyNumericFeature):
    def __init__(self, Graph, ApkFile):
        LOG.info('initilizing')
        apk = ApkFile
        graph = Graph
        PhylogenyNumericFeature.__init__(self, graph, apk, 'age-from-root')
        LOG.info('done initializing %s', self.name)
    def compute_feature(self):
        malware = self.malware
        graph = self.phylogeny
        child_node = graph.get_node(str(malware))
        root = graph.get_root()[0]
        if root == child_node:
            age = 0
        else:
            age_extractor = NodesAge(root, child_node)
            age = age_extractor.get_age()
        self.value = age
class NodeAgeFromLatest(PhylogenyNumericFeature):
    def __init__(self, Graph, ApkFile, LastApkFile):
        LOG.info('initilizing')
        self.lastsample = LastApkFile
        apk = ApkFile
        graph = Graph
        PhylogenyNumericFeature.__init__(self, graph, apk, 'age-from-latest')
        LOG.info('done initializing %s', self.name)
    def compute_feature(self):
        malware = self.malware
        graph = self.phylogeny
        lastsample = self.lastsample
        node = graph.get_node(str(malware))
        last_node = graph.get_node(str(lastsample))
        if node == last_node:
            age = 0
        else:
            age_extractor = NodesAge(node, last_node)
            age = age_extractor.get_age()
        self.value = age
class AgeLatestChild(PhylogenyNumericFeature):
    def __init__(self, Graph, ApkFile):
        LOG.info('initilizing')
        apk = ApkFile
        graph = Graph
        PhylogenyNumericFeature.__init__(self, graph, apk, 'age-of-latest-child')
        LOG.info('done initializing %s', self.name)
    def compute_feature(self):
        malware = self.malware
        graph = self.phylogeny
        node = graph.get_node(str(malware))
        successors = graph.successors(node)
        if len(successors) == 0:
            age = 0
        else:
            successors_tuples = []
            for s in successors:
                date_attr = s.attr['comment']
                successor_date = datetime.strptime(date_attr,'%Y-%m-%d %H:%M:%S')
                successors_tuples.append((s, successor_date))
            sorted_list = sorted(successors_tuples, key=lambda successor:successor[1], reverse=True)
            newest_child = sorted_list[0][0]
            age_extractor = NodesAge(node, newest_child)
            age = age_extractor.get_age()
        self.value = age
class AgeNewestDescendant(PhylogenyNumericFeature):
    def __init__(self, Graph, ApkFile):
        LOG.info('initilizing')
        apk = ApkFile
        graph = Graph
        PhylogenyNumericFeature.__init__(self, graph, apk, 'age-of-neweset-descendant')
        LOG.info('done initializing %s', self.name)
    def compute_feature(self):
        malware = self.malware
        graph = self.phylogeny
        parent = graph.get_node(str(malware))
        mybfs = Bfs(graph, str(malware))
        all_descendants = mybfs.getDescendants()
        if len(all_descendants) == 0:
            age = 0
        else:
            successors_tuples = []
            for s in all_descendants:
                date_attr = s.attr['comment']
                successor_date = datetime.strptime(date_attr,'%Y-%m-%d %H:%M:%S')
                successors_tuples.append((s, successor_date))
            sorted_list = sorted(successors_tuples, key=lambda successor:successor[1], reverse=True)
            newest_successor = sorted_list[0][0]
            age_extractor = NodesAge(parent, newest_successor)
            age = age_extractor.get_age()
        self.value = age



    

        
        

'''
Created on Nov 3, 2010

@author: edwards
'''
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from xml.dom import minidom
from datamining.apps.reporting.models import Committee, Role, Affiliation
from django.template import NodeList
from datamining.apps.profiles.models import Staff
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class Node(object):
    def __init__(self, id, label, type):
        self.id = id
        self.label = label
        self.type = type
        self.duplicate_of = None
        
    def is_duplicate(): #@NoSelf
        doc = """Checks to see if this node is a duplicate""" #@UnusedVariable
       
        def fget(self):
            return self.duplicate_of is not None
           
        return locals()
    
    def __str__(self):
        return "(%s)%s" % (self.type[0],self.label)

    def __unicode__(self):
        return u"(%s)%s" % (self.type[0],self.label)
       
    is_duplicate = property(**is_duplicate())

class Edge(object):
    def __init__(self, id, source_id, target_id):
        self.id = id
        self.source_id = source_id
        self.target_id = target_id
        self.source = None
        self.target = None
        self.redundant = False
        
    def link(self,dict):
        if dict.has_key(self.source_id) and dict.has_key(self.target_id):
            self.source = dict[self.source_id]
            self.target = dict[self.target_id]
            if self.source.is_duplicate:
                self.source = self.source.duplicate_of
            if self.target.is_duplicate:
                self.target = self.target.duplicate_of
            if self.source == self.target:
                self.redundant = True
        
    def is_linked(): #@NoSelf
        doc = """Shows whether this edge has been linked""" #@UnusedVariable
       
        def fget(self):
            return (self.source is not None) and (self.target is not None)
                      
        return locals()
       
    def __str__(self):
        return "%s --> %s" % (self.source,self.target)

    def __unicode__(self):
        return u"%s --> %s" % (self.source,self.target)
       
    is_linked = property(**is_linked())

class Command(BaseCommand):
    args = ''
    help = 'Imports person and committee data from a yfiles resource'

    def handle(self, *args, **options):
        xmldoc = minidom.parse(args[0])
        graphml = xmldoc.getElementsByTagName("graphml")[0]
        graphs = graphml.getElementsByTagName("graph")
        node_elements = NodeList()
        edge_elements = NodeList()
        nodes = {}
        names = {}
        edges = {}
        for graph in graphs:
            node_elements += graph.getElementsByTagName("node")
            edge_elements += graph.getElementsByTagName("edge")
        for node in node_elements:
            attrs = node.attributes
            data = node.getElementsByTagName("data")
            label = None
            for datum in data:
                labels = datum.getElementsByTagName("y:NodeLabel")
                if len(labels) > 0:
                    if labels[0].parentNode.nodeName == "y:GroupNode":
                        label = " ".join(labels[0].childNodes[0].toxml().split("\n"))
                        type = "committee"
                        break
                    elif labels[0].parentNode.nodeName == "y:ShapeNode":
                        label = labels[0].childNodes[0].toxml().split("\n")[-1]
                        if label == "":
                            label = labels[0].childNodes[0].toxml().split("\n")[-2]
                        type = "person"
                        break
            if label is not None and label.strip() != "Faculty":
                new_node = Node(attrs['id'].value,label,type)
                nodes[attrs['id'].value] = new_node
                if names.has_key(label):
                    new_node.duplicate_of = names[label]
                else:
                    names[label] = new_node
            if attrs['id'].value.find('::') >= 0:
                parent_id = attrs['id'].value.split('::')[0]
                child_id = attrs['id'].value
                edges[parent_id + '::' + child_id] = Edge(parent_id + '::' + child_id,child_id,parent_id)
                
#                        committee = Committee()
#                        com_is_duplicatemittee.name = committee_name
#                        print committee 
        for edge in edge_elements:
            attrs = edge.attributes
            if nodes.has_key(attrs['source'].value) and nodes.has_key(attrs['target'].value): 
                edges[attrs['id'].value] = Edge(attrs['id'].value,attrs['source'].value,attrs['target'].value)
            #print edge.toxml()

        clean_edges = {}
        for edge in edges.values():
            edge.link(nodes)
            if edge.is_linked and not edge.redundant and not clean_edges.has_key(str(edge)):
                clean_edges[str(edge)] = edge
        
        creator = User.objects.get(username="admin")
        committee_type = ContentType.objects.get(name="Committee")
        person_type = ContentType.objects.get(name="Person")
        member = Role.objects.get(title="member",content_type=committee_type)
        manager = Role.objects.get(title="manager",content_type=person_type)
        
        for edge in clean_edges.values():
            if edge.source.type == "committee":
                source,created = Committee.objects.get_or_create(title=edge.source.label,created_by=creator)
            else:
                names = edge.source.label.split()
                if len(names) > 1:
                    source,created = Staff.objects.get_or_create(first_name=names[0],last_name=names[1],created_by=creator)
            
            if edge.target.type == "committee":
                target,created = Committee.objects.get_or_create(title=edge.target.label,created_by=creator)
            else:
                names = edge.target.label.split()
                if len(names) > 1:
                    target,created = Staff.objects.get_or_create(first_name=names[0],last_name=names[1],created_by=creator)
            
            if isinstance(source, Staff) and isinstance(target, Committee):
                aff,created = Affiliation.objects.get_or_create(person=source,object_id=target.id,content_type=committee_type,role=member,created_by=creator)
            elif isinstance(source, Staff) and isinstance(target, Staff):
                aff,created = Affiliation.objects.get_or_create(person=source,object_id=target.id,content_type=person_type,role=manager,created_by=creator)
            
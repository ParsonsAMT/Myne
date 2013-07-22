from django.core.management.base import BaseCommand, CommandError
from datamining.apps.profiles.models import FacultyMember, Expertise
import networkx as nx
import matplotlib.pyplot as plt
import operator

class Command(BaseCommand):
    args = 'output_file'
    help = 'Generates a graph of faculty based on expertise linkages'

    def handle(self, *args, **options):
        members = FacultyMember.actives.filter(expertise__facultymember__isnull=False).distinct()
        graph1 = nx.Graph()
        for member in members:
            graph1.add_node(member.full_name())
            for area in member.expertise.all():
                if not graph1.has_node(area.name):
                    graph1.add_node(area.name)
                graph1.add_edge(member.full_name(),area.name)
        expertise = Expertise.objects.all()
        
        #cores = nx.find_cores(graph1)
        
        #sorted_cores = sorted(cores.iteritems(),key=operator.itemgetter(1))
        
        #print sorted_cores
        
        graph2 = nx.Graph()

        for area in expertise:
            if graph1.has_node(area.name):
                a_node = graph1[area.name]
                subgraph = nx.Graph()
                keys = a_node.keys()
                subgraph.add_nodes_from(keys)
                for index,node in enumerate(keys):
                    for v in range(index+1,len(keys)):
                        weight = 1
                        if graph2.has_edge(node,keys[v]):
                            graph2.edge[node][keys[v]]["weight"] += 1
                        if subgraph.has_edge(node,keys[v]):
                            subgraph.edge[node][keys[v]]["weight"] = weight
                        else:
                            subgraph.add_edge(node,keys[v],weight=weight)
                #subgraph = nx.complete_graph(0,create_using=subgraph)
                graph2 = nx.compose(graph2,subgraph)
                
        for edge in graph2.edges():
            print edge, graph2[edge[0]][edge[1]]["weight"]
            if graph2[edge[0]][edge[1]]["weight"] == 1:
                graph2.remove_edge(edge[0],edge[1])
                
        cores = nx.find_cores(graph2)
        
        sorted_cores = sorted(cores.iteritems(),key=operator.itemgetter(1))
        
#        id = 0
#        for core in sorted_cores:
#            if core[1] != id:
#                print "=" * 20,
#                print core[1],
#                print "=" * 20                
#                id = core[1]
#            print core[0],
#            if core[1] == 0:
#                print "(no k-core)"
#            else:
#                print
        
        import graphutils
        
        graph2,subs = graphutils.computeSubgraphClusters(nx.connected_component_subgraphs(graph2)[0],0,100)
        
        agraph = nx.to_agraph(graph2)

        for index,sub in enumerate(subs):
            sub = agraph.subgraph(nbunch=sub.nodes(), 
                             name="cluster%d" % (index), 
                             style='filled', 
                             color='#ccccff', 
                             fontcolor='#000033',
                             fontname="Gotham Rounded",
                             splines="true",
                             label='cluster %d' % (index + 1)) 

        if len(args) > 1:
            #agraph = nx.to_agraph(graph2)
            #agraph.graph_attr.update(layout="neato",bgcolor="#000000", bb = "0,0,822,810", viewport="1440,810,1,411,405", overlap="scale")
            agraph.graph_attr.update(layout="fdp",bgcolor="#ffffff", overlap="scale", splines="true", bb="10,7.5", size="10,7.5", page="11,8.5", maxiter="2400")
            try:
                agraph.node_attr.update(color="#000033",fontcolor="#000033", shape="plaintext", fontsize="10", fontname="Gotham Rounded")
            except:
                agraph.node_attr.update(color="#000033",fontcolor="#000033", shape="plaintext", fontsize="10")
            agraph.edge_attr.update(color="#333366",fontcolor="#333333", arrowhead="dot", arrowtail="dot", arrowsize="0.5")
            agraph.layout(prog="fdp")
                                                                  
            agraph.draw(args[1], format="pdf")
            agraph.write(args[0])
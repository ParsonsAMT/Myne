'''
Created on Aug 6, 2010

@author: edwards
'''
import networkx as nx
from operator import itemgetter
#does heuristic clustering
def computeSubgraphClusters(G,start=0,divisions=2):
    edged_subgraphs = len(nx.connected_component_subgraphs(G))
    while edged_subgraphs < divisions:
        for pair in reversed(sorted(nx.edge_betweenness(G).iteritems(), key=itemgetter(1))[-1:]):
            G.remove_edge(pair[0][0], pair[0][1])
        new_subgraphs = nx.connected_component_subgraphs(G)
        proposed_subgraphs = []
        for subgraph in new_subgraphs:
            if len(subgraph.nodes()) > 1:
                proposed_subgraphs.append(subgraph)
            else:
                break
        #if we start losing clusters, stop
        #no guarantee we haven't hit a local maximum
        if len(proposed_subgraphs) < edged_subgraphs:
            break
        subgraphs = proposed_subgraphs
        edged_subgraphs = len(subgraphs)   
        print edged_subgraphs

    for index, subgraph in enumerate(subgraphs):
        s0 = nx.Graph()
        s0.add_edges_from(subgraph.edges(data=True))
        print
        print subgraph.nodes(data=True)
#        attrs = ["fillcolor", "style", "shape", "fontsize", "fontname", "fontcolor"]
#        for node in subgraph.nodes(data=True):
#            node_attr = {}
#            for attr in attrs:
#                node_attr[attr] = node[1][attr]
#
#            s0.node[node[0]] = node_attr

        #print s0.nodes(data=True)
        noteSubgraph = nx.to_agraph(s0)
        #print subgraph
        #print noteSubgraph.node_attr
        #noteSubgraph.graph_attr.update(bgcolor="#ffffff", overlap="scale", splines="true", size="10.5,8", dpi="96", maxiter="2400") #noteSubgraph.node_attr.update(fontsize="15", color="#666666", style="filled", fillcolor=colors[data[0]], fontcolor="white", fontname="Tuffy", shape="box")
        #noteSubgraph.layout(prog="neato")
        #noteSubgraph.draw("noteSubgraph%d.png" % (index + 1 + start), format="png")

    return G,subgraphs
